"""REST client handling, including GetPocketStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Union, cast
import logging
import backoff
import time
import pytz
from dateutil.parser import isoparse
import datetime
import ciso8601

from memoization import cached

from singer import utils
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_getpocket.auth import GetPocketAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
STATE = {}

logger = logging.getLogger(__name__)


class UserRateLimitExceeded(Exception):
    def __init__(self, response):
        logger.error(response.headers['X-Error'])
        self.response = response


class KeyRateLimitExceeded(Exception):
    def __init__(self, response):
        logger.error(response.headers['X-Error'])
        self.response = response


class GetPocketStream(RESTStream):
    """GetPocket stream class."""

    url_base = "https://getpocket.com/v3/get"
    records_jsonpath = "$.list.*"

    @property
    @cached
    def authenticator(self) -> GetPocketAuthenticator:
        """Return a new authenticator object."""
        return GetPocketAuthenticator.create_for_stream(self)

    def wait(err=None):
        if isinstance(err, UserRateLimitExceeded):
            delay = int(err.response.headers['X-Limit-User-Reset'])
            logging.info('waiting for {}s until reset'.format(delay))
        elif isinstance(err, KeyRateLimitExceeded):
            delay = int(err.response.headers['X-Limit-Key-Reset'])
            logging.info('waiting for {}s until reset'.format(delay))
        else:
            raise err
        time.sleep(delay)

    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.RequestException, UserRateLimitExceeded, KeyRateLimitExceeded),
        max_tries=5,
        giveup=wait,
        factor=2,
    )
    def _request_with_backoff(
            self, prepared_request: requests.PreparedRequest, context: Optional[dict]
    ) -> requests.Response:
        response = self.requests_session.send(prepared_request)
        headers = response.headers

        if self._LOG_REQUEST_METRICS:
            extra_tags = {}
            if self._LOG_REQUEST_METRIC_URLS:
                extra_tags["url"] = cast(str, prepared_request.path_url)
            self._write_request_duration_log(
                endpoint=self.path,
                response=response,
                context=context,
                extra_tags=extra_tags,
            )
        if response.status_code == 401:
            self.logger.info(
                f"Reason: {response.status_code} - {str(response.content)}"
            )
            self.logger.info("Failed request for {}".format(prepared_request.url))

            logging.error(headers['X-Error'])
            raise RuntimeError("Requested resource was unauthorized or not found.")
        elif response.status_code == 403:
            logging.debug(headers)
            if 'X-Limit-User-Remaining' in headers and headers['X-Limit-User-Remaining'] == '-1':
                raise UserRateLimitExceeded(response)
            elif 'X-Limit-Key-Remaining' in headers and headers['X-Limit-Key-Remaining'] == '-1':
                raise KeyRateLimitExceeded(response)
            else:
                raise RuntimeError("Requested resource was forbidden or not found.")
        elif response.status_code >= 400:
            raise RuntimeError(
                f"Error making request to API: {prepared_request.url} "
                f"[{response.status_code} - {str(response.content)}]".replace(
                    "\\n", "\n"
                )
            )

        logger.debug('Rate limit enforced per user: {} ({} remaining)'.format(headers['X-Limit-User-Limit'],
                                                                              headers['X-Limit-User-Remaining']))
        logger.debug('Rate limit enforced per consumer key: {} ({} remaining)'.format(headers['X-Limit-Key-Limit'],
                                                                                      headers['X-Limit-Key-Remaining']))
        logger.debug("Response received successfully.")
        return response

    def get_start(self):
        if self.replication_key not in STATE or (STATE[self.replication_key]) < self.config.get('start_date'):
            STATE[self.replication_key] = self.config.get('start_date')
        return STATE[self.replication_key]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:

        if self.config.get('favorite') is None:
            logger.info('Getting all items (favorited and un-favorited)')
        elif self.config.get('favorite') == 1:
            logger.info('Only getting favorited items')
        elif self.config.get('favorite') == 0:
            logger.info('Only getting un-favorited items')
        else:
            raise ValueError('Invalid value for "favorite" setting, should be 0, 1 or empty')

        # not sure if this is the best place, but STATE needs to be updated
        if self.replication_key not in STATE:
            # if this is available, use it
            if self.get_context_state(context).get('replication_key_value'):
                STATE[self.replication_key] = self.get_context_state(context).get('replication_key_value')
            else:
                STATE[self.replication_key] = self.get_start()
        else:
            logger.info('self.replication_key: {}'.format(STATE[self.replication_key]))

        since = STATE[self.replication_key]
        unix_since = unix_ts(since)
        logger.info(since)
        logger.info(unix_since)

        """Return a dictionary of values to be used in URL parameterization."""
        # api does not support sorting by replication key. sorting from oldest to newest as recommended
        params: dict = {'sort': 'oldest',
                        'since': unix_since
                        }

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""

        # sort by ascending update date
        # update date is not always available (for very old articles, must be a "new" feature)
        # TODO: if update date is not available, always include
        r = response.json()

        # TODO this is not docuented on the api, but one request is limited to 5000 records.
        #  so if metric record count = 5000 the pipeline should alwas run again (state will guarantee that missing
        # records are fetched

        # the api only allows to sort by time_added, not by time_updated (the replication_key)
        # TODO can not sort if update date  not available
        sort_index = sorted(r['list'], key=lambda x: (r['list'][x].get('time_updated', '0'),
                                                      r['list'][x].get('time_updated', '0'))
                            )
        index_map = {v: i for i, v in enumerate(sort_index)}
        r['list'] = dict(sorted(r['list'].items(), key=lambda pair: index_map[pair[0]]))

        # the api parameter "since" is >=, ie it includes the last state (from the last record)
        # to avoid last article to duplicate, remove it time_updated == STATE
        # warning: state is datetime_str while time updated is unix timestamp
        logging.info(r['list'][sort_index[0]].get('time_updated', '0') == str(unix_ts(STATE[self.replication_key])))
        if r['list'][sort_index[0]].get('time_updated', '0') == str(unix_ts(STATE[self.replication_key])):
            logging.info('first record is equal to state!')
            del r['list'][sort_index[0]]

        yield from extract_jsonpath(self.records_jsonpath, input=r)

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        if 'time_updated' not in row:
            row['time_updated'] = self.schema.get('properties').get('time_updated').get('default')

        for k, v in row.items():
            formatted = format_timestamp(v, type(v), self.schema.get('properties').get(k))
            row[k] = formatted
            logging.debug('{} before: {}, after: {}'.format(k, v, formatted))

        return row


    def parse_datetime(datetime_str):
        dt = isoparse(datetime_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=pytz.UTC)
        return dt


def format_timestamp(data, typ, schema):
    result = data
    if data and isinstance(data, str) and data != '0' and schema.get('format') == 'date-time':
        utc_dt = datetime.datetime.utcfromtimestamp(int(data)).replace(tzinfo=pytz.UTC)
        result = utils.strftime(utc_dt)

    return result

def unix_ts(datetime_str):
    return int(ciso8601.parse_datetime(datetime_str).timestamp())

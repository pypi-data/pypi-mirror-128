"""REST client handling, including GetPocketStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, cast
import logging
import backoff
import time
import pytz
import datetime
import ciso8601

from memoization import cached

from singer import utils
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_getpocket.auth import GetPocketAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
TRUTHY = ("true", "1", "yes", "on")
FALSY = ("false", "0", "no", "off")
STATE = {}

logger = logging.getLogger(__name__)


class UserRateLimitExceeded(Exception):
    """
    Custom exception raised when user rate limit exceeded ('X-Limit-User-Remaining'<0)
    """
    def __init__(self, response):
        logger.error(response.headers['X-Error'])
        self.response = response


class KeyRateLimitExceeded(Exception):
    """
    Custom exception raised when user key rate limit exceeded ('X-Limit-Key-Remaining'<0)
    """
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
        """
        used by @backoff to wait until rate reset
        :return:
        """
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

    def get_start(self) -> str:
        """
        Get date threshold to extract data. If no STATE is available or STATE is prior to start_date from config, use
        start date defined in config (by user or default)
        :return:
        """
        if self.replication_key not in STATE or (STATE[self.replication_key]) < self.config.get('start_date'):
            STATE[self.replication_key] = self.config.get('start_date')
        return STATE[self.replication_key]

    def get_setting_favorite(self) -> Optional[int]:
        """
        Get favorite setting from config (or default), and do some basic validation
        The valid values for the API are None, 0 and 1
        If something goes wrong, all records are retrieved
        :return:
        """
        favorite = self.config.get('favorite')
        try:
            if favorite is None:
                logger.info('Getting all items (favorited and un-favorited)')
            elif truthy(self.config.get('favorite')):
                logger.info('Only getting favorited items')
                favorite = 1
            elif falsy(self.config.get('favorite')):
                favorite = 0
                logger.info('Only getting un-favorited items')
            else:
                raise ValueError('Invalid value for "favorite" setting, should be 0, 1 or empty')
        except Exception as err:
            logger.warning(err)
            logger.warning('Invalid setting for "favorite", returning all records')
            return None
        else:
            return favorite

    def get_setting_state(self) -> str:
        """
        Get state setting from config (or default), and do some basic validation
        The valid values for the API are 'all', 'unread' and 'archive'
        If something goes wrong, all records are retrieved
        :return:
        """
        state = self.config.get('state')
        try:
            if state is None:
                logger.info('Getting all items (unread and archived)')
            elif state.lower() == 'unread':
                logger.info('Only getting unread items')
                state = 'unread'
            elif state.lower() in ('archive', 'archived', 'read'):
                logger.info('Only getting archived items')
                state = 'archive'
            else:
                raise ValueError('Invalid value for "state" setting, should be "all", "read" or "archive"')
        except Exception as err:
            logger.warning(err)
            logger.warning('Invalid setting for "state", returning all records')
            return 'all'
        else:
            return state

    def get_setting_detail_type(self) -> str:
        """
        Get detail_type setting from config (or default), and do some basic validation
        The valid values for the API are 'simple' (return basic info about each item) and 'complete' (return all data)
        If something goes wrong, "complete" is used
        :return:
        """
        detail_type = self.config.get('detail_type')
        try:
            if detail_type is None:
                logger.info('Getting complete data from items')
                detail_type = 'complete'
            elif detail_type.lower() in ('basic', 'less'):
                logger.info('Only getting basic info from data')
                detail_type = 'basic'
            elif detail_type.lower() in ('complete', 'more'):
                logger.info('Getting full info from data')
                detail_type = 'complete'
            else:
                raise ValueError('Invalid value for "detail_type" setting, should be "basic" or "complete"')
        except Exception as err:
            logger.warning(err)
            logger.warning('Invalid setting for "detail_type", returning complete data from items')
            return 'complete'
        else:
            return detail_type

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """

        :param context:
        :param next_page_token:
        :return:
        """

        if self.replication_key not in STATE:
            # get appropriate STATE to consider as threshold to extract new records
            if self.get_context_state(context).get('replication_key_value'):
                STATE[self.replication_key] = self.get_context_state(context).get('replication_key_value')
            else:
                STATE[self.replication_key] = self.get_start()
        else:
            logger.info('self.replication_key: {}'.format(STATE[self.replication_key]))

        since = STATE[self.replication_key]
        logger.info('Considered threshold to extract records: {}'.format(since))

        """Return a dictionary of values to be used in URL parameterization."""
        # api does not support sorting by replication key. sorting from oldest to newest as recommended
        params: dict = {'sort': 'oldest',
                        'since': unix_ts(since),
                        'favorite': self.get_setting_favorite(),
                        'state': self.get_setting_state(),
                        'detailType': self.get_setting_detail_type(),
                        'tag': self.config.get('tag'),
                        }

        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO this is not documented on the api, but one request is limited to 5000 records.
        # so if metric record count = 5000 the pipeline should always run again (STATE will guarantee that missing
        # records are fetched)
        r = response.json()

        if len(r['list']) == 0:
            logger.warning('No records found for current settings / state')
        else:
            # drop all records marked as "to be deleted" (status=2)
            delete_index = [k for k, v in r['list'].items() if r['list'][k].get('status') == '2']
            logger.debug('Invalid records found to be deleted: {}'.format(delete_index))
            for del_key in delete_index:
                del r['list'][del_key]

            # sort by ascending update date
            # the api only allows to sort by time_added, not by time_updated (the replication_key)
            # update date is not always available (for very old articles, must be a "new" feature)
            # If update date is empty, consider 0
            sort_index = sorted(r['list'], key=lambda x: (r['list'][x].get('time_updated', '0'),
                                                          r['list'][x].get('time_updated', '0'))
                                )
            index_map = {v: i for i, v in enumerate(sort_index)}
            r['list'] = dict(sorted(r['list'].items(), key=lambda pair: index_map[pair[0]]))

            # the api parameter "since" is >=, ie it includes the last STATE (from the last record)
            # to avoid last article to duplicate, remove it time_updated == STATE
            # warning: STATE is datetime_str while time updated is unix timestamp
            if r['list'][sort_index[0]].get('time_updated', '0') == str(unix_ts(STATE[self.replication_key])):
                logging.info('Removing duplicated record with update_date equal to STATE!')
                del r['list'][sort_index[0]]

        yield from extract_jsonpath(self.records_jsonpath, input=r)

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """
        Convert date-time fields from unix to ISO time string
        :param row:
        :param context:
        :return:
        """
        if 'time_updated' not in row:
            row['time_updated'] = self.schema.get('properties').get('time_updated').get('default')

        for k, v in row.items():
            logger.debug('Processing {}'.format(k))
            try:
                formatted = format_type(v, self.schema.get('properties').get(k))
            except:
                # if this fails continue with original value
                pass
            else:
                row[k] = formatted
            logging.debug('{} before: {}, after: {}'.format(k, v, formatted))

        # if item not in row, use default value
        try:
            properties = self.schema.get('properties')
            for prop in properties:
                if prop not in row:
                    logger.debug('Property {} not found in result'.format(prop))
                    logger.debug('Using default value: {}'.format(properties.get(prop).get('default')))
                    # if no default is defined, default value is None
                    row[prop] = properties.get(prop).get('default')
        except:
            # if this fails, return original row
            pass

        return row


def format_type(value, schema):
    """

    :param value:
    :param schema:
    :return:
    """
    result = value
    if result and isinstance(result, str) and schema.get('format') == 'date-time':
        # make sure date time fields are formatted as such
        if result != '0':
            utc_dt = datetime.datetime.utcfromtimestamp(int(result)).replace(tzinfo=pytz.UTC)
            result = utils.strftime(utc_dt)
        else:
            # date not available, return None
            result = None
    if result and isinstance(result, str) and 'integer' in schema.get('type'):
        # make sure integer fields are formatted as such
        result = int(result)
    if result and isinstance(result, str) and 'boolean' in schema.get('type'):
        # make sure boolean fields are formatted as such
        # string 0 is converted to True, so make sure we evaluate truthy here before
        result = truthy(result)
    return result


def unix_ts(datetime_str: str) -> int:
    """

    :param datetime_str:
    :return:
    """
    return int(ciso8601.parse_datetime(datetime_str).timestamp())


def truthy(val) -> bool:
    """
    Convert user input that evaluates to True into boolean True, considering the following truthy values:
    TRUTHY = ("true", "1", "yes", "on")
    :param val:
    :return:
    """
    return str(val).lower() in TRUTHY


def falsy(val) -> bool:
    """
    Convert user input that evaluates to False into boolean False, considering the following falsy values:
    FALSY = ("false", "0", "no", "off")
    :param val:
    :return:
    """
    return str(val).lower() in FALSY

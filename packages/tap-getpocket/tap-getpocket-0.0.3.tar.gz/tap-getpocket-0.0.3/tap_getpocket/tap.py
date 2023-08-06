"""GetPocket tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_getpocket.streams import (
    ContentStream,
)

STREAM_TYPES = [
    ContentStream,
]


class TapGetPocket(Tap):
    """GetPocket tap class."""
    name = "tap-getpocket"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "consumer_key",
            th.StringType,
            required=True,
            description="The consumer key used in the authentication flow"
        ),
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="Access token to authenticate against the API service. Follow instructions in README to get"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            default='2010-01-01T00:00:00Z',
            required=False,
            description="The earliest record date to sync"
        ),
        th.Property(
            "favorite",
            th.BooleanType,
            default=None,
            required=False,
            description="Whether to retrieve only favorited, unforited or all items"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

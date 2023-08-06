"""Stream type classes for tap-getpocket."""

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_getpocket.client import GetPocketStream


class ContentStream(GetPocketStream):
    """Define custom stream."""
    name = "list"
    path = "/./"
    primary_keys = ["item_id"]
    replication_key = "time_updated"
    # Schemas solve the limited data types problem providing more information about how to interpret JSON's basic types
    schema = th.PropertiesList(
        th.Property("item_id", th.StringType, required=True),
        th.Property("resolved_id", th.StringType),
        th.Property("given_url", th.StringType),
        th.Property("resolved_url", th.StringType),
        th.Property("given_title", th.StringType),
        th.Property("resolved_title", th.StringType),
        th.Property("favorite", th.BooleanType),
        th.Property("status", th.IntegerType),
        th.Property("excerpt", th.StringType),
        th.Property("is_article", th.BooleanType),
        th.Property("has_image", th.BooleanType),
        th.Property("has_video", th.BooleanType),
        th.Property("word_count", th.IntegerType),
        th.Property("time_updated", th.DateTimeType),
        th.Property("time_added", th.DateTimeType),
        th.Property("time_read", th.DateTimeType),
        th.Property("time_favorited", th.DateTimeType),
        th.Property("sort_id", th.IntegerType),
        th.Property("is_index", th.BooleanType),
        th.Property("lang", th.StringType),
        th.Property("listen_duration_estimate", th.IntegerType),
        th.Property("time_to_read", th.IntegerType),
        th.Property("amp_url", th.StringType),
        th.Property("top_image_url", th.StringType),
        th.Property("tags",
                    th.ObjectType(
                        th.Property("item_id", th.IntegerType),
                        th.Property("tag", th.StringType)
                    )),
        th.Property("authors",
                    th.ObjectType(
                        th.Property("item_id", th.IntegerType),
                        th.Property("author_id", th.IntegerType),
                        th.Property("name", th.StringType),
                        th.Property("url", th.StringType),
                    )),
        th.Property("domain_metadata",
                    th.ObjectType(
                        th.Property("greyscale_logo", th.StringType),
                        th.Property("logo", th.StringType),
                        th.Property("name", th.StringType),
                                )
                    ),
        th.Property("image",
                    th.ObjectType()),
        th.Property("images",
                    th.ObjectType()),
        th.Property("videos", th.ObjectType()),
    ).to_dict()

"""GetPocket Authentication."""


from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
import logging

logger = logging.getLogger(__name__)

# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class GetPocketAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for GetPocket.."""

    # meltano config tap-getpocket list

    @property
    def auth_params(self) -> dict:
        # access token in config.json is only found if explicitly invoked
        # otherwise this is always reading from meltano.yml
        if not self.config.get('access_token'):
            logger.critical('No access token available. Run authentication flow according to README')
        return {"consumer_key": self.config.get('consumer_key'),
                "access_token": self.config.get('access_token')
                }

    @property
    def auth_headers(self) -> dict:
        return {'Content-Type': 'application/json',
                "X-Accept": "application/json",
                "charset": 'utf-8'}

    @classmethod
    def create_for_stream(cls, stream) -> "GetPocketAuthenticator":
        return cls(
            stream=stream
        )

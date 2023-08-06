import ssl
from typing import Any, Dict, Optional, Tuple, Union

import httpx
import websockets.client
from loguru import logger
from semver import VersionInfo

from classiq_interface import __version__ as classiq_interface_version
from classiq_interface.server import authentication
from classiq_interface.server.routes import ROUTE_PREFIX

from classiq import config
from classiq._version import VERSION as CLASSIQ_VERSION
from classiq.authentication import token_manager
from classiq.exceptions import ClassiqAPIError, ClassiqExpiredTokenError

_PROCESSED_VERSION = Union[VersionInfo, str]
_PROCESSED_VERSIONS = Tuple[_PROCESSED_VERSION, _PROCESSED_VERSION]


_VERSION_UPDATE_SUGGESTION = (
    'Run "pip install -U <PACKAGE>==<REQUIRED VERSION>" to resolve the conflict.'
)


class Client:
    _UNKNOWN_VERSION = "0.0.0"

    def __init__(self, conf: config.Configuration):
        self._config = conf
        self._token_manager = token_manager.TokenManager()
        self._ssl_context = ssl.create_default_context()
        self._HTTP_TIMEOUT_SECONDS = (
            3600  # Needs to be synced with load-balancer timeout
        )

    @staticmethod
    def _handle_response(response: httpx.Response) -> Union[Dict, str]:
        if response.is_error:
            expired = (
                response.status_code == httpx.codes.UNAUTHORIZED
                and response.json()["detail"] == authentication.EXPIRED_TOKEN_ERROR
            )

            if expired:
                raise ClassiqExpiredTokenError("Expired token.")

            raise ClassiqAPIError(
                f"Call to API failed with code {response.status_code}: "
                f"{response.json()['detail']}"
            )

        return response.json()

    def _make_client_args(self) -> Dict[str, Any]:
        return {
            "base_url": self._config.host,
            "timeout": self._HTTP_TIMEOUT_SECONDS,
            "headers": self._get_authorization_header(),
        }

    async def call_api(
        self, http_method: str, url: str, body: Optional[Dict] = None
    ) -> Union[Dict, str]:
        async with httpx.AsyncClient(**self._make_client_args()) as async_client:
            response = await async_client.request(
                method=http_method, url=url, json=body
            )
            return self._handle_response(response)

    def sync_call_api(
        self, http_method: str, url: str, body: Optional[Dict] = None
    ) -> Union[Dict, str]:
        with httpx.Client(**self._make_client_args()) as sync_client:
            response = sync_client.request(method=http_method, url=url, json=body)
            return self._handle_response(response)

    def _get_authorization_header(self) -> Dict:
        access_token = self._token_manager.access_token
        if access_token is None:
            return dict()
        return {"Authorization": f"Bearer {access_token}"}

    def _get_authorization_query_string(self) -> str:
        access_token = self._token_manager.access_token
        if access_token is None:
            return ""
        return f"?token={access_token}"

    def save_tokens(self, access_token: str, refresh_token: Optional[str]) -> None:
        self._token_manager.save_tokens(access_token, refresh_token)

    def is_refresh_token_available(self) -> bool:
        return self._token_manager.is_refresh_token_available()

    def update_expired_access_token(self) -> None:
        self._token_manager.update_expired_access_token()

    def establish_websocket_connection(self, path: str) -> websockets.client.connect:
        _MAX_PAYLOAD_SIZE = 2 ** 23  # = 8MiB ~= 8MB

        return websockets.client.connect(
            uri=f"{self._config.ws_uri}{path}{self._get_authorization_query_string()}",
            ssl=self._ssl_context if self._config.ws_uri.scheme == "wss" else None,
            max_size=_MAX_PAYLOAD_SIZE,
        )

    def get_backend_uri(self):
        return self._config.host

    def _get_host_version(self) -> str:
        versions: Dict[str, str] = self.sync_call_api("get", f"{ROUTE_PREFIX}/versions")
        return versions["classiq_interface"]

    @classmethod
    def _check_matching_versions(
        cls, lhs_version: str, rhs_version: str, normalize: bool = True
    ) -> bool:
        if normalize:
            # VersionInfo comparison is compatible with strings but it excludes any build info
            processed_versions = VersionInfo.parse(lhs_version), VersionInfo.parse(
                rhs_version
            )
        else:
            processed_versions = lhs_version, rhs_version
        processed_versions: _PROCESSED_VERSIONS
        if cls._UNKNOWN_VERSION in processed_versions:
            # In case one of those versions is unknown, they are considered equal
            logger.debug(
                "Either {} or {} is an unknown version. Assuming both versions are equal.",
                lhs_version,
                rhs_version,
            )
            return True
        return processed_versions[0] == processed_versions[1]

    def check_host(self) -> None:
        # This function is NOT async (despite the fact that it can be) because it's called from a non-async context.
        # If this happens when we already run in an event loop (e.g. inside a call to asyncio.run), we can't go in to
        # an async context again.
        # Since this function should be called ONCE in each session, we can handle the "cost" of blocking the
        # event loop.
        if not self._check_matching_versions(
            classiq_interface_version, CLASSIQ_VERSION, normalize=False
        ):
            # When raising an exception, use the original strings
            raise ClassiqAPIError(
                f"Classiq API version mismatch: 'classiq' version is {CLASSIQ_VERSION}, "
                f"'classiq-interface' version is {classiq_interface_version}. {_VERSION_UPDATE_SUGGESTION}"
            )
        raw_host_version = self._get_host_version()
        if not self._check_matching_versions(
            raw_host_version, classiq_interface_version
        ):
            raise ClassiqAPIError(
                f"Classiq API version mismatch: 'classiq-interface' version is "
                f"{classiq_interface_version}, backend version is {raw_host_version}. {_VERSION_UPDATE_SUGGESTION}"
            )


DEFAULT_CLIENT: Optional[Client] = None


def client() -> Client:
    global DEFAULT_CLIENT
    if DEFAULT_CLIENT is None:
        # This call initializes DEFAULT_CLIENT
        configure(config.init())

    return DEFAULT_CLIENT


def configure(conf: config.Configuration) -> None:
    global DEFAULT_CLIENT
    assert DEFAULT_CLIENT is None, "Can not configure client after first usage."

    DEFAULT_CLIENT = Client(conf=conf)
    if conf.should_check_host:
        DEFAULT_CLIENT.check_host()

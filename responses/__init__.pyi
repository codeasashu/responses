from collections import Sequence
from collections import Sized
from io import BufferedReader
from io import BytesIO
from re import Pattern
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union
from typing import overload
from unittest import mock as std_mock
from urllib.parse import quote as quote

from requests.adapters import HTTPResponse
from requests.adapters import PreparedRequest
from requests.cookies import RequestsCookieJar
from typing_extensions import Literal

# Not currently exposed in typestubs, thus, ignore
from urllib3.response import HTTPHeaderDict  # type: ignore

from .matchers import json_params_matcher
from .matchers import urlencoded_params_matcher

def _clean_unicode(url: str) -> str: ...
def _ensure_str(s: str) -> str: ...
def _ensure_url_default_path(
    url: Union[Pattern[str], str]
) -> Union[Pattern[str], str]: ...
def _get_url_and_path(url: str) -> str: ...
def _handle_body(
    body: Optional[Union[bytes, BufferedReader, str]]
) -> Union[BufferedReader, BytesIO]: ...
def _has_unicode(s: str) -> bool: ...
def _is_string(s: Union[Pattern[str], str]) -> bool: ...
def get_wrapped(
    func: Callable[..., Any], responses: RequestsMock, registry: Optional[Any]
) -> Callable[..., Any]: ...

class Call(NamedTuple):
    request: PreparedRequest
    response: Any

_Body = Union[str, BaseException, "Response", BufferedReader, bytes]

MatcherIterable = Iterable[Callable[[Any], Callable[..., Any]]]

class CallList(Sequence[Call], Sized):
    def __init__(self) -> None:
        self._calls = List[Call]
        ...
    def __iter__(self) -> Iterator[Call]: ...
    def __len__(self) -> int: ...
    def __getitem__(self, idx: int) -> Call: ...  # type: ignore [override]
    def add(self, request: PreparedRequest, response: _Body) -> None: ...
    def reset(self) -> None: ...

class FalseBool:
    def __bool__(self) -> bool: ...

class BaseResponse:
    passthrough: bool = ...
    content_type: Optional[str] = ...
    headers: Optional[Mapping[str, str]] = ...
    stream: bool = ...
    method: Any = ...
    url: Any = ...
    match_querystring: Any = ...
    match: MatcherIterable = ...
    call_count: int = ...
    def __init__(
        self,
        method: str,
        url: Union[Pattern[str], str],
        match_querystring: Union[bool, object] = ...,
        match: MatcherIterable = ...,
    ) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def _req_attr_matches(
        self, match: MatcherIterable, request: PreparedRequest
    ) -> Tuple[bool, str]: ...
    def _should_match_querystring(
        self, match_querystring_argument: Union[bool, object]
    ) -> bool: ...
    def _url_matches(
        self, url: Union[Pattern[str], str], other: str, match_querystring: bool = ...
    ) -> bool: ...
    def _url_matches_strict(self, url: str, other: str) -> bool: ...
    def get_headers(self) -> HTTPHeaderDict: ...  # type: ignore
    def get_response(self, request: PreparedRequest) -> None: ...
    def matches(self, request: PreparedRequest) -> Tuple[bool, str]: ...

class Response(BaseResponse):
    body: _Body = ...
    status: int = ...
    headers: Optional[Mapping[str, str]] = ...
    stream: bool = ...
    content_type: Optional[str] = ...
    auto_calculate_content_length: bool = ...
    def __init__(
        self,
        method: str,
        url: Union[Pattern[str], str],
        body: _Body = ...,
        json: Optional[Any] = ...,
        status: int = ...,
        headers: Optional[Mapping[str, str]] = ...,
        stream: bool = ...,
        content_type: Optional[str] = ...,
        auto_calculate_content_length: bool = ...,
        match_querystring: bool = ...,
        match: MatcherIterable = ...,
    ) -> None: ...
    def get_response(  # type: ignore [override]
        self, request: PreparedRequest
    ) -> HTTPResponse: ...

class CallbackResponse(BaseResponse):
    callback: Callable[[Any], Any] = ...
    stream: bool = ...
    content_type: Optional[str] = ...
    def __init__(
        self,
        method: str,
        url: Union[Pattern[str], str],
        callback: Callable[[Any], Any],
        stream: bool = ...,
        content_type: Optional[str] = ...,
        match_querystring: Union[bool, FalseBool] = ...,
        match: MatcherIterable = ...,
    ) -> None: ...
    def get_response(  # type: ignore [override]
        self, request: PreparedRequest
    ) -> HTTPResponse: ...

class PassthroughResponse(BaseResponse):
    passthrough: bool = ...

class OriginalResponseShim:
    msg: Any = ...
    def __init__(  # type: ignore [no-any-unimported]
        self, headers: HTTPHeaderDict
    ) -> None: ...
    def isclosed(self) -> bool: ...

_F = TypeVar("_F", bound=Callable[..., Any])

class RequestsMock:
    DELETE: Literal["DELETE"]
    GET: Literal["GET"]
    HEAD: Literal["HEAD"]
    OPTIONS: Literal["OPTIONS"]
    PATCH: Literal["PATCH"]
    POST: Literal["POST"]
    PUT: Literal["PUT"]
    response_callback: Optional[Callable[[Any], Any]] = ...
    assert_all_requests_are_fired: Any = ...
    passthru_prefixes: Tuple[Union[str, Pattern[str]], ...] = ...
    target: Any = ...
    _matches: List[Any]
    _registry: Any
    def __init__(
        self,
        assert_all_requests_are_fired: bool = ...,
        response_callback: Optional[Callable[[Any], Any]] = ...,
        passthru_prefixes: Tuple[str, ...] = ...,
        target: str = ...,
        registry: Any = ...,
    ) -> None:
        self._patcher = Callable[[Any], Any]
        self._calls = CallList
        ...
    def reset(self) -> None: ...
    add: _Add
    delete: _Shortcut
    get: _Shortcut
    head: _Shortcut
    options: _Shortcut
    patch: _Shortcut
    post: _Shortcut
    put: _Shortcut
    add_passthru: _AddPassthru
    def remove(
        self,
        method_or_response: Optional[Union[str, Response]] = ...,
        url: Optional[Union[Pattern[str], str]] = ...,
    ) -> None: ...
    replace: _Replace
    upsert: _Upsert
    add_callback: _AddCallback
    @property
    def calls(self) -> CallList: ...
    def __enter__(self) -> RequestsMock: ...
    def __exit__(self, type: Any, value: Any, traceback: Any) -> bool: ...
    def activate(self, func: Optional[_F], registry: Optional[Any]) -> _F: ...
    def start(self) -> None: ...
    def stop(self, allow_assert: bool = ...) -> None: ...
    def assert_call_count(self, url: str, count: int) -> bool: ...
    def registered(self) -> List[Any]: ...
    def _set_registry(self, registry: Any) -> None: ...
    def get_registry(self) -> Any: ...

HeaderSet = Optional[Union[Mapping[str, str], List[Tuple[str, str]]]]

class _Add(Protocol):
    def __call__(
        self,
        method: Optional[Union[str, BaseResponse]] = ...,
        url: Optional[Union[Pattern[str], str]] = ...,
        body: _Body = ...,
        json: Optional[Any] = ...,
        status: int = ...,
        headers: HeaderSet = ...,
        stream: bool = ...,
        content_type: Optional[str] = ...,
        auto_calculate_content_length: bool = ...,
        adding_headers: HeaderSet = ...,
        match_querystring: bool = ...,
        match: MatcherIterable = ...,
    ) -> None: ...

class _Shortcut(Protocol):
    def __call__(
        self,
        url: Optional[Union[Pattern[str], str]] = ...,
        body: _Body = ...,
        json: Optional[Any] = ...,
        status: int = ...,
        headers: HeaderSet = ...,
        stream: bool = ...,
        content_type: Optional[str] = ...,
        auto_calculate_content_length: bool = ...,
        adding_headers: HeaderSet = ...,
        match_querystring: bool = ...,
        match: MatcherIterable = ...,
    ) -> None: ...

class _AddCallback(Protocol):
    def __call__(
        self,
        method: str,
        url: Union[Pattern[str], str],
        callback: Callable[
            [PreparedRequest], Union[Exception, Tuple[int, Mapping[str, str], _Body]]
        ],
        match_querystring: bool = ...,
        content_type: Optional[str] = ...,
        match: MatcherIterable = ...,
    ) -> None: ...

class _AddPassthru(Protocol):
    def __call__(self, prefix: Union[Pattern[str], str]) -> None: ...

class _Remove(Protocol):
    def __call__(
        self,
        method_or_response: Optional[Union[str, BaseResponse]] = ...,
        url: Optional[Union[Pattern[str], str]] = ...,
    ) -> None: ...

class _Replace(Protocol):
    def __call__(
        self,
        method_or_response: Optional[Union[str, BaseResponse]] = ...,
        url: Optional[Union[Pattern[str], str]] = ...,
        body: _Body = ...,
        json: Optional[Any] = ...,
        status: int = ...,
        headers: HeaderSet = ...,
        stream: bool = ...,
        content_type: Optional[str] = ...,
        adding_headers: HeaderSet = ...,
        match_querystring: bool = ...,
        match: MatcherIterable = ...,
    ) -> None: ...

class _Upsert(Protocol):
    def __call__(
        self,
        method: Optional[Union[str, BaseResponse]] = ...,
        url: Optional[Union[Pattern[str], str]] = ...,
        body: _Body = ...,
        json: Optional[Any] = ...,
        status: int = ...,
        headers: HeaderSet = ...,
        stream: bool = ...,
        content_type: Optional[str] = ...,
        adding_headers: HeaderSet = ...,
        match_querystring: bool = ...,
        match: MatcherIterable = ...,
    ) -> None: ...

class _Registered(Protocol):
    def __call__(self) -> List[Response]: ...

class _Activate(Protocol):
    # see https://github.com/getsentry/responses/pull/469 for more details

    @overload
    def __call__(self, func: _F = ...) -> _F: ...
    # use this overload for scenario when 'responses.activate' is used

    @overload
    def __call__(self, registry: Type[Any] = ...) -> Callable[["_F"], "_F"]: ...
    # use this overload for scenario when 'responses.activate(registry=)' is used

activate: _Activate
add: _Add
add_callback: _AddCallback
add_passthru: _AddPassthru
assert_all_requests_are_fired: bool
assert_call_count: Callable[[str, int], bool]
calls: CallList
delete: _Shortcut
DELETE: Literal["DELETE"]
get: _Shortcut
GET: Literal["GET"]
head: _Shortcut
HEAD: Literal["HEAD"]
mock: RequestsMock
_default_mock: RequestsMock
options: _Shortcut
OPTIONS: Literal["OPTIONS"]
passthru_prefixes: Tuple[str, ...]
patch: _Shortcut
PATCH: Literal["PATCH"]
post: _Shortcut
POST: Literal["POST"]
put: _Shortcut
PUT: Literal["PUT"]
registered: _Registered
remove: _Remove
replace: _Replace
reset: Callable[[], None]
response_callback: Callable[[Any], Any]
start: Callable[[], None]
stop: Callable[..., None]
target: Any
upsert: _Upsert

__all__ = [
    "CallbackResponse",
    "Response",
    "RequestsMock",
    # Exposed by the RequestsMock class:
    "activate",
    "add",
    "add_callback",
    "add_passthru",
    "assert_all_requests_are_fired",
    "assert_call_count",
    "calls",
    "delete",
    "DELETE",
    "get",
    "GET",
    "head",
    "HEAD",
    "options",
    "OPTIONS",
    "passthru_prefixes",
    "patch",
    "PATCH",
    "post",
    "POST",
    "put",
    "PUT",
    "registered",
    "remove",
    "replace",
    "reset",
    "response_callback",
    "start",
    "stop",
    "target",
    "upsert",
]

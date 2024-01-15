from typing import Literal

import requests
from requests.structures import CaseInsensitiveDict

from . import utils


HTMLMethod = Literal['GET', 'HEAD', 'POST', 'PUT', 'PATH', 'DELETE', 'OPTIONS']


class Response:
    def __init__(
        self,
        *,
        status: int,
        headers: dict[str, str] | CaseInsensitiveDict,
        body: str,
    ):
        assert isinstance(status, int)
        utils.assert_headers(headers)
        assert isinstance(headers, dict) or isinstance(headers, CaseInsensitiveDict)
        assert isinstance(body, str)

        headers = {k.lower(): v for k,v in headers.items()}

        self.status = status
        self.headers = headers
        self.body = body


    def __str__(self) -> str:
        return f"{self.status}\n{self.headers}\n{self.body}"


    @property
    def content_type(self) -> str:
        return self.headers.get('content-type', '').lower()


class Request:
    def __init__(
        self,
        *,
        method: HTMLMethod,
        url: str,
    ):
        method = method.upper()
        assert method in HTMLMethod.__args__
        assert isinstance(url, str)


        self._method: HTMLMethod = method
        self._url = url
        self._headers: dict[str, str] = {}
        self._body: str | None = None


    def __str__(self) -> str:
        return f'{self._method} {self._url}\n{self._headers}\n\n{self._body}'


    @property
    def url(self) -> str:
        if self._url.startswith('http'):
            return self._url
        return 'https://' + self._url


    def add_header(self, key: str, value: str):
        assert isinstance(key, str)
        assert isinstance(value, str)

        self._headers[key.lower().strip()] = value.strip()


    def add_body(self, body: str):
        assert isinstance(body, str)

        self._body = body.strip()


    def send(self) -> Response:
        r = requests.request(
            method=self._method,
            url=self.url,
            headers=self._headers,
            data=self._body,
        )

        return Response(
            status=r.status_code,
            headers=r.headers,
            body=r.text,
        )



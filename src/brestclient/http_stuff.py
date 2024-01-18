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
        self.variable_names: list[str] = []
        self._variables: dict[str, str] = {}


    def __str__(self) -> str:
        return f'{self._method} {self._url}\n{self._headers}\n\n{self._body}'


    @property
    def url(self) -> str:
        if self._url.startswith('http'):
            return self._url
        return 'https://' + self._url


    def set_variable_value(self, var: str, value: str):
        if var in self.variable_names:
            self._variables[var] = value


    def add_header(self, key: str, value: str):
        assert isinstance(key, str)
        assert isinstance(value, str)

        self._headers[key.lower().strip()] = value.strip()


    def add_body(self, body: str):
        assert isinstance(body, str)

        self._body = body.strip()


    def _with_placed_values(self, text: str | None) -> str | None:
        if not text:
            return text

        # TODO: optimize, it would be slow
        result = text
        for var, value in self._variables.items():
            placeholder = f'{{{{{var}}}}}'
            value_txt = f'{value}'

            result = result.replace(placeholder, value_txt)
        return result


    def send(self) -> Response:
        url = self._with_placed_values(self._url)
        headers = {self._with_placed_values(k): self._with_placed_values(v) for k, v in self._headers.items()}
        body = self._with_placed_values(self._body)

        r = requests.request(
            method=self._method,
            url=url,
            headers=headers,
            data=body,
        )

        return Response(
            status=r.status_code,
            headers=r.headers,
            body=r.text,
        )



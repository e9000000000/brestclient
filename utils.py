from requests.structures import CaseInsensitiveDict


def assert_headers(headers: dict[str, str] | CaseInsensitiveDict):
    assert isinstance(headers, dict) or isinstance(headers, CaseInsensitiveDict)
    for key, value in headers.items():
        assert isinstance(key, str)
        assert isinstance(value, str)

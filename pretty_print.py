import json


def pretty_format_headers(headers: dict[str, str]) -> str:
    assert isinstance(headers, dict)
    return '\n'.join([f'{k}: {v}' for k, v in headers.items()])


def pretty_format_body(body: str, content_type: str) -> str:
    assert isinstance(body, str)
    assert isinstance(content_type, str)

    if 'application/json' in content_type:
        return json.dumps(json.loads(body), indent=4, ensure_ascii=False)
    else:
        return body


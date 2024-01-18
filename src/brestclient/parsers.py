from dataclasses import dataclass
import re
import traceback

from .http_stuff import Request
from .request_picker import RequestPicker
from .variables import Variables


@dataclass
class File:
    request_picker: RequestPicker
    variables: Variables


def parse_request(text: str) -> Request:
    '''parse part of a file, just one request, with comments and name removed'''

    assert isinstance(text, str)

    lines = text.splitlines()
    method_and_url_parts = lines[0].split()

    request = Request(
        method=method_and_url_parts[0],
        url=' '.join(method_and_url_parts[1:]),
    )

    for i, line in enumerate(lines[1:]):
        if line == '':
            request.add_body('\n'.join(lines[i+1:]))
            break

        key_value = line.split(':')
        if len(key_value) != 2:
            raise ValueError(f'invalid header {line=}')
        key, value = key_value[0], key_value[1]
        request.add_header(key.strip(), value.strip())

    var_names = parse_variable_names(text)
    request.variable_names = var_names

    return request


def parse_variable_names(text: str) -> list[str]:
    assert isinstance(text, str)

    placeholders = re.findall(r'\{\{[^\}]+\}\}', text)
    return [p[2:-2] for p in placeholders]


def parse_variables(text: str) -> Variables:
    assert isinstance(text, str)

    names = parse_variable_names(text)
    return Variables(names=names)


def parse_file(file_path: str) -> File:
    '''parse whole file'''

    request_picker = RequestPicker()

    with open(file_path, 'r') as f:
        text = f.read()


    variables = parse_variables(text)

    regex = re.compile(r'^###.*?(?=^###|\Z)', re.MULTILINE | re.DOTALL)
    raw_requests = regex.findall(text)

    for raw_request in raw_requests:
        try:
            lines = raw_request.splitlines()
            end_of_comments = 0
            for line in lines:
                if line.startswith('#'):
                    end_of_comments += 1
                else:
                    break

            name = lines[0][3:].strip()
            raw_request_without_comments = '\n'.join(lines[end_of_comments:])
            request = parse_request(raw_request_without_comments)
            request_picker.add_request(
                name=name,
                request=request,
            )
        except:
            print(f"ERROR: can't parse this request:\n{raw_request}\n")
            traceback.print_exc()

    return File(
        variables=variables,
        request_picker=request_picker,
    )

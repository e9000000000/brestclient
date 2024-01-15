import re

from .http_stuff import Request
from .request_picker import RequestPicker


def parse_request(text: str) -> Request:
    '''
    text syntax is simple:
    first line: METHOD URL
    all next lines until empty line: HEADER_KEY: HEADER_VALUE
    empty line:
    all lines till the end are lines of a request body

    METHOD - can be any html method, case does not matter

    URL - any valid http url, if protocol is not specified (google.com for example)
    it will be a https protocol

    headers - all what is left of : is a header key, all is right of : - header value
    both will be striped

    body will be striped as one big line

    example:
    POST google.com?q=weffwe
    Authorization: Bearer foj23fjjf03jf3029jf30jf3029j23f09
    content-type: application/json

    {
        "something": [1, 2, 3],
        "please_collect_all_my_data": true
    }
    '''

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

    return request


def parse_file(file_path: str) -> RequestPicker:
    '''
    reads file content and parse it

    file syntax:
    ### request name, description and stuff
    # it's matter to have no spaces before ###
    # all next lines started with # is a comments, will be ignored
    # it's matter to use ### only in the begining of request
    # cuz ### means a request start, for comments use # or ##
    REQUEST (syntax described in parse_request docstring)

    then any amount of empty lines, all of them will be striped

    ### next request name...
    ...

    '''

    request_picker = RequestPicker()

    with open(file_path, 'r') as f:
        text = f.read()

    regex = re.compile(r'^###.*?(?=^###|\Z)', re.MULTILINE | re.DOTALL)
    raw_requests = regex.findall(text)

    for raw_request in raw_requests:
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

    return request_picker

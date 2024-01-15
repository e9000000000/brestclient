import argparse

from . import parsers
from . import pretty_print as pp


def run():
    parser = argparse.ArgumentParser(
        prog='Better rest clinet (brestclient)',
        description='Just the best terminal rest client',
    )
    parser.add_argument(
        'filepath',
        help='path to the file with http requests',
    )
    parser.add_argument(
        '-q',
        '--query',
        help='query to find request by it\'s name, case does\'t matter',
    )

    args = parser.parse_args()

    request_picker = parsers.parse_file(args.filepath)

    if args.query:
        request = request_picker.find(args.query)
        if request is None:
            print(f'can\'t find request by given {args.query=}')
            exit(1)
    else:
        print('Pick a request by number')
        for i, name in request_picker.enumerate():
            print(f'{i}: {name}')

        number = int(input('> '))
        request = request_picker.get(number)

    response = request.send()
    headers = pp.pretty_format_headers(response.headers)
    body = pp.pretty_format_body(response.body, response.content_type)
    print(f'\n\n{response.status}\n{headers}\n\n{body}')

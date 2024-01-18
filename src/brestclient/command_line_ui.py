import argparse

from . import parsers
from . import pretty_print as pp


def print_request_list(request_picker: parsers.RequestPicker):
    for i, name in request_picker.enumerate():
        print(f'{i}: {name}')


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
        help='query to find and perform request by it\'s name, case does\'t matter',
    )
    parser.add_argument(
        '-l',
        '--list',
        help='prints list of request numerated names and exits',
        action='store_true',
    )
    parser.add_argument(
        '-n',
        '--request-number',
        help='number of a request which will be performed, then program will exit',
        type=int,
    )

    args = parser.parse_args()

    file = parsers.parse_file(args.filepath)
    request_picker = file.request_picker
    variables = file.variables

    if args.list:
        print_request_list(request_picker)
        exit(0)


    # chouse a request
    if args.query:
        request = request_picker.find(args.query)
        if request is None:
            print(f'can\'t find request by given {args.query=}')
            exit(1)
    elif args.request_number:
        request = request_picker.get(args.request_number)
    else:
        print('Pick a request by number')
        print_request_list(request_picker)

        number = int(input('> '))
        request = request_picker.get(number)


    # perform
    request_variables = variables.get_variables_and_saved_values_for_request(request)
    for v, saved_val in request_variables:
        val = input(f'{v} ({saved_val}): ')
        if val != saved_val and val != '':
            variables.set_variable(v, val)

    variables.set_request_variable_values(request)

    response = request.send()
    headers = pp.pretty_format_headers(response.headers)
    body = pp.pretty_format_body(response.body, response.content_type)
    print(f'\n\n{response.status}\n{headers}\n\n{body}')

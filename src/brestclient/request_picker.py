from .http_stuff import Request


class RequestPicker:
    def __init__(self):
        self._requests = {}
        self._enumerated = []


    def __str__(self) -> str:
        return f'\n\n{"-"*80}\n\n'.join(f'### {name}\n{request}' for name, request in self._requests.items())


    def add_request(
        self,
        *,
        name: str,
        request: Request,
    ):
        assert isinstance(name, str)
        assert isinstance(request, Request)

        self._requests[name] = request
        self._enumerated.append(name)

    
    def find(self, query: str) -> Request | None:
        '''search request by request_name contains query, case does't matter'''

        assert isinstance(query, str)

        query = query.lower()

        for name, request in self._requests.items():
            if query in name.lower():
                return request


    def enumerate(self) -> list[tuple[int, str]]:
        '''
        return list of (number, request_name)

        you can get request by this number in get method
        '''

        return [(i+1, name) for i, name in enumerate(self._enumerated)]


    def get(self, number: int) -> Request:
        return self._requests[self._enumerated[number - 1]]



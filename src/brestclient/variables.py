import tempfile
from pathlib import Path

from .http_stuff import Request


TEMP_DIR = tempfile.gettempdir()
TEMP_FILEPATH = Path(TEMP_DIR) / 'brestclient_saved_variables'
DELIMETR = '--&__^_^__&--'


class Variables:
    def __init__(self, *, names: list[str]):
        assert isinstance(names, list)
        for name in names:
            assert isinstance(name, str)

        saved = self._get_saved_values()
        self._values = {n: saved.get(n, '') for n in names}


    def _get_saved_values(self) -> dict[str, str]:
        saved = {}
        try:
            with open(TEMP_FILEPATH, 'r') as f:
                for line in f.read().splitlines():
                    sp = line.split(DELIMETR)
                    saved[sp[0]] = sp[1]
        except FileNotFoundError:
            pass  # not file - nothign to do
        return saved

    def set_request_variable_values(self, request: Request):
        for var, value in self._values.items():
            request.set_variable_value(var, value)


    def get_variables_and_saved_values_for_request(self, request: Request) -> list[tuple]:
        return [(n, self._values[n]) for n in request.variable_names]


    def set_variable(self, name: str, value: str):
        assert isinstance(name, str)
        assert isinstance(value, str)

        self._values[name] = value

        with open(TEMP_FILEPATH, 'w') as f:
            f.write('\n'.join(f'{n}{DELIMETR}{v}' for n, v in self._values.items()))

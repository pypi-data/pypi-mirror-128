from typing import Any


class Configuration:
    def __init__(self, **kwargs) -> None:
        self._config = kwargs

    def get(self, arg: str) -> Any:
        try:
            assert arg in self._config.keys()
        except AssertionError:
            raise KeyError(f"Configuration has no argument {arg}")
        return self._config.get(arg)

    def set(self, arg: str, value: Any) -> None:
        self._config.update({arg: value})

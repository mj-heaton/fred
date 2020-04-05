from os import getenv


class FredConfig:

    @staticmethod
    def _string_to_bool(value: str) -> bool:
        value = str(value)

        valid = {
            "yes": True,
            "y": True,
            "ye": True,
            "no": False,
            "n": False,
            "true": True,
            "false": False
        }

        value = value.strip().lower()

        if value not in valid:
            raise ValueError(f'Error, invalid bool config argument: {value}')

        return valid[value]

    def _get_lower_strip_env(key: str, default: str=None) -> str:
        return str(getenv(key, default=default)).strip().lower()

    def __init__(self):
        self.FRED_DISTRIBUTED_MODE = \
            self._string_to_bool(getenv('FRED_DISTRIBUTED_MODE', 'false'))

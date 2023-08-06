from typing import Any


class ToSnug:
    """
    Main class for converting dictionary objects into the snug source
    """

    def __init__(self, data: dict) -> None:
        self.data: dict = data
        self.collected: str = ""

    def __to_snug_type(self, key: str, val: Any) -> str:
        if isinstance(val, str):
            return "\"{}\" ".format(val)
        elif val is None:
            return "nil "
        elif isinstance(val, list):
            return "[{}] ".format(" ".join(self.__to_snug_type(None, i) for i in val))
        elif isinstance(val, dict):
            collected = "({} ".format(key if key is not None else "?")

            for (k, v) in val.items():
                if isinstance(v, dict):
                    collected += self.__to_snug_type(k, v)
                else:
                    collected += "{} {}".format(k, self.__to_snug_type(key, v))

            return "{}) ".format(collected)
        else:
            return "{} ".format(val)

    def convert(self):
        """
        Convert dictionary to the snug source and save it to the "collected" data member
        """

        for (key, value) in self.data.items():
            if isinstance(value, dict):
                self.collected += self.__to_snug_type(key, value)
            else:
                self.collected += "{} {}".format(key,
                                                 self.__to_snug_type(key, value))

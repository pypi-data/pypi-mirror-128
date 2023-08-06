from .lexer import *
from .to_snug import *
from .transpiler import *
from json import loads as json_loads


def load_as_json(file_path: str) -> str:
    """
    Load a snug file and convert into JSON 
    """

    with open(file_path, "r") as f:
        file_data = f.read()

    lexer = Lexer(file_data)
    lexer.lexerize()

    transpiler = Transpiler(lexer.tokens)
    transpiler.to_json()

    return transpiler.json


def loads_as_json(data: str) -> str:
    """
    Load a snug source and convert into JSON 
    """

    lexer = Lexer(data)
    lexer.lexerize()

    transpiler = Transpiler(lexer.tokens)
    transpiler.to_json()

    return transpiler.json


def load(file_path: str) -> dict:
    """
    Load a snug file and convert into dictionary 
    """

    with open(file_path, "r") as f:
        file_data = f.read()

    lexer = Lexer(file_data)
    lexer.lexerize()

    transpiler = Transpiler(lexer.tokens)
    transpiler.to_json()

    return json_loads(transpiler.json)


def loads(data: str) -> dict:
    """
    Load a snug source and convert into dictionary 
    """

    lexer = Lexer(data)
    lexer.lexerize()

    transpiler = Transpiler(lexer.tokens)
    transpiler.to_json()

    return json_loads(transpiler.json)


def dumps(data: dict) -> str:
    """
    Convert dictionary to the snug source
    """

    converter = ToSnug(data)
    converter.convert()

    return converter.collected


def dump(data: dict, file_path: str):
    """
    Convert dictionary to the snug source and write to the file
    """

    converter = ToSnug(data)
    converter.convert()

    with open(file_path, "w+", encoding="utf-8") as f:
        f.write(converter.collected)

from typing import List
from .lexer import Token, Types


class Transpiler:
    """
    Transpile the snug source to the JSON.
    """

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.ignore_indexs: List[int] = []
        self.json: str = "{"

    def __value_converter(self, token: Token):
        if token.type == Types.STRING:
            return "\"{}\"".format(token.value)
        elif token.type == Types.INTEGER:
            return str(token.value)
        elif token.type == Types.FLOAT:
            return str(float(token.value))
        elif token.type == Types.BOOLEAN_YES:
            return "true"
        elif token.type == Types.BOOLEAN_NO:
            return "false"
        elif token.type == Types.NIL:
            return "null"

    def __get_token(self, index: int) -> Token:
        if index < len(self.tokens):
            return self.tokens[index]

        raise SyntaxError(
            "SyntaxError: Token not found for index: {}".format(index))

    def __parse_anonymous_object(self, given_index: int):
        """
        Parse anonymous object to the JSON
        """

        self.json += "{"

        for index in range(given_index, len(self.tokens)):
            token = self.tokens[index]

            # Check if index is already visited
            if index in self.ignore_indexs:
                continue
            else:
                self.ignore_indexs.append(index)

            if token.type == Types.OBJECT_OPEN:
                self.__parse_object(index, token)
            elif token.type == Types.BRACKET_OPEN:
                self.__parse_array(index)
            elif token.type == Types.OBJECT_CLOSE:
                if self.tokens[index-1].type != Types.ANONYMOUS_OBJECT_OPEN and self.json[-1] != "}":
                    self.json = self.json[:len(self.json)-1] + "},"
                else:
                    self.json += "},"

                break
            elif token.type == Types.UNKNOWN and not self.__get_token(index+1).type in (Types.BRACKET_OPEN, Types.OBJECT_OPEN, Types.ANONYMOUS_OBJECT_OPEN):
                self.json += "\"{}\":{},".format(
                    token.value, self.__value_converter(self.__get_token(index+1)))

    def __parse_anonymous_array(self, given_index: int):
        """
        Parse anonymous array to the JSON
        """

        self.json += "["

        for index in range(given_index+1, len(self.tokens)):
            token = self.tokens[index]

            # Check if index is already visited
            if index in self.ignore_indexs:
                continue
            else:
                self.ignore_indexs.append(index)

            if token.type == Types.ANONYMOUS_OBJECT_OPEN:
                self.__parse_anonymous_object(index)
            if token.type == Types.BRACKET_OPEN:
                self.__parse_anonymous_array(index)
            elif token.type == Types.BRACKET_CLOSE:
                if self.tokens[index-1].type != Types.BRACKET_OPEN:
                    self.json = self.json[:len(self.json)-1] + "],"
                else:
                    self.json += "],"

                break

            if self.__value_converter(token) is not None:
                self.json += "{},".format(self.__value_converter(token))
            elif token.type == Types.UNKNOWN:
                raise TypeError(
                    "TypeError: Type not found for {} <{}>".format(token, token.value))

    def __parse_array(self, given_index: int):
        """
        Parse array to the JSON
        """

        self.json += "\"{}\":[".format(self.tokens[given_index-1].value)

        for index in range(given_index+1, len(self.tokens)):
            token = self.tokens[index]

            # Check if index is already visited
            if index in self.ignore_indexs:
                continue
            else:
                self.ignore_indexs.append(index)

            if token.type == Types.ANONYMOUS_OBJECT_OPEN:
                self.__parse_anonymous_object(index)
            if token.type == Types.BRACKET_OPEN:
                self.__parse_anonymous_array(index)
            elif token.type == Types.BRACKET_CLOSE:
                if self.tokens[index-1].type != Types.BRACKET_OPEN:
                    self.json = self.json[:len(self.json)-1] + "],"
                else:
                    self.json += "],"

                return

            if self.__value_converter(token) is not None:
                self.json += "{},".format(self.__value_converter(token))
            elif token.type == Types.UNKNOWN:
                raise TypeError(
                    "TypeError: Type not found for {} <{}>".format(token, token.value))

    def __parse_object(self, given_index: int, given_token: Token):
        """
        Parse object to the JSON
        """

        self.json += "\"{}\":{{".format(given_token.value)

        for index in range(given_index, len(self.tokens)):
            token = self.tokens[index]

            # Check if index is already visited
            if index in self.ignore_indexs:
                continue
            else:
                self.ignore_indexs.append(index)

            if token.type == Types.OBJECT_OPEN:
                self.__parse_object(index, token)
            elif token.type == Types.BRACKET_OPEN:
                self.__parse_array(index)
            elif token.type == Types.OBJECT_CLOSE:
                if self.tokens[index-1].type != Types.ANONYMOUS_OBJECT_OPEN and self.json[-1] != "}":
                    self.json = self.json[:len(self.json)-1] + "},"
                else:
                    self.json += "},"

                break
            elif token.type == Types.UNKNOWN and not self.__get_token(index+1).type in (Types.BRACKET_OPEN, Types.OBJECT_OPEN, Types.ANONYMOUS_OBJECT_OPEN):
                self.json += "\"{}\":{},".format(
                    token.value, self.__value_converter(self.__get_token(index+1)))

    def to_json(self):
        """
        Transpile snug source to the JSON
        """

        for (index, token) in enumerate(self.tokens):
            # Check if index is already visited
            if index in self.ignore_indexs:
                continue
            else:
                self.ignore_indexs.append(index)

            # Parsing
            if token.type == Types.OBJECT_OPEN:
                self.__parse_object(index, token)
            elif token.type == Types.BRACKET_OPEN:
                self.__parse_array(index)
            elif token.type == Types.UNKNOWN and not self.__get_token(index+1).type in (Types.BRACKET_OPEN, Types.OBJECT_OPEN, Types.ANONYMOUS_OBJECT_OPEN):
                self.json += "\"{}\":{},".format(
                    token.value, self.__value_converter(self.__get_token(index+1)))

        if self.json[-1] == "}":
            self.json += "}"
        else:
            self.json = self.json[:len(self.json)-1] + "}"

from typing import Final, List


class Types:
    """
    Static class for store type literals
    """

    NIL: Final[int] = 0

    BRACKET_OPEN: Final[int] = 1
    BRACKET_CLOSE: Final[int] = 2

    OBJECT_OPEN: Final[int] = 3
    ANONYMOUS_OBJECT_OPEN: Final[int] = 4
    OBJECT_CLOSE: Final[int] = 5

    INTEGER: Final[int] = 6
    FLOAT: Final[int] = 7
    STRING: Final[int] = 8

    BOOLEAN_YES: Final[int] = 9
    BOOLEAN_NO: Final[int] = 10

    UNKNOWN: Final[int] = 11


class Token:
    """
    Token struct for store key-value
    """

    def __init__(self, type: int, value: str) -> None:
        self.type: int = type
        self.value: str = value


class Lexer:
    """
    Lexer class for tokenizing the original data and store the found tokens
    """

    def __init__(self, data: str) -> None:
        self.data: str = data + " \n "
        self.collected_token: str = ""

        self.collecting_string: bool = False
        self.collecting_comment: bool = False
        self.collecting_literal: bool = False

        self.tokens: List[Token] = []

    def __can_integer(self, value: str) -> bool:
        value = value.replace("_", "")

        try:
            int(value)
            return True
        except Exception:
            return False

    def __can_float(self, value: str) -> bool:
        found_dot = 0
        found_num = 0

        for i in value:
            if i in "0123456789":
                found_num += 1
            elif i == ".":
                found_dot += 1
            elif i == "_":
                pass
            else:
                return False

        return found_dot == 1 and found_num == len(value) - 1

    def __collect_literal(self):
        self.collected_token = self.collected_token.replace("\n", "")

        if len(self.collected_token) == 0:
            return

        if self.__can_integer(self.collected_token):
            self.tokens.append(
                Token(Types.INTEGER, self.collected_token.replace("_", "")))
        elif self.__can_float(self.collected_token):
            self.tokens.append(
                Token(Types.FLOAT, self.collected_token.replace("_", "")))
        elif self.collected_token == "yes":
            self.tokens.append(Token(Types.BOOLEAN_YES, ""))
        elif self.collected_token == "no":
            self.tokens.append(Token(Types.BOOLEAN_NO, ""))
        elif self.collected_token == "(?":
            self.tokens.append(Token(Types.ANONYMOUS_OBJECT_OPEN, ""))
        elif self.collected_token[0] == "(":
            self.tokens.append(
                Token(Types.OBJECT_OPEN, self.collected_token[1:]))
        elif self.collected_token == "nil":
            self.tokens.append(Token(Types.NIL, ""))
        else:
            self.tokens.append(Token(Types.UNKNOWN, self.collected_token))

        self.collected_token = ""
        self.collecting_literal = False

    def lexerize(self):
        for (index, value) in enumerate(self.data):
            if (not self.collecting_string) and (not self.collecting_comment):
                if value == "[":
                    self.__collect_literal()
                    self.tokens.append(Token(
                        Types.BRACKET_OPEN, ""
                    ))
                elif value == "]":
                    self.__collect_literal()
                    self.tokens.append(Token(
                        Types.BRACKET_CLOSE, ""
                    ))
                elif value == ")":
                    self.__collect_literal()
                    self.tokens.append(Token(
                        Types.OBJECT_CLOSE, ""
                    ))
                elif value == "\"":
                    self.__collect_literal()
                    self.collecting_string = True
                elif value == "#":
                    self.collecting_comment = True
                elif value == "\r":
                    pass
                elif value in (" ", "\n", "\t"):
                    self.__collect_literal()
                else:
                    self.collecting_literal = True
                    self.collected_token += value
            elif not self.collecting_comment:
                if value == "\"":
                    if self.data[index-1] == "\\":
                        self.collected_token += "\\\""
                    else:
                        self.tokens.append(
                            Token(Types.STRING, self.collected_token))

                        self.collecting_string = False
                        self.collected_token = ""
                else:
                    self.collected_token += value
            else:
                if value == "#":
                    self.collecting_comment = False

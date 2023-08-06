from enum import Enum


class _EnumStr(Enum):
    def __str__(self):
        return self.name.lower()


class Colors(_EnumStr):
    GREY = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


class Highlights(_EnumStr):
    ON_GREY = 40
    ON_RED = 41
    ON_GREEN = 42
    ON_YELLOW = 43
    ON_BLUE = 44
    ON_MAGENTA = 45
    ON_CYAN = 46
    ON_WHITE = 47


class Attributes(_EnumStr):
    BOLD = 1
    DARK = 2
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    CONCEALED = 8

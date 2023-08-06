# coding: utf-8
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Aidan Chaplin

"""ANSII Color formatting for output in terminal."""

from __future__ import print_function
import os
import re
from typing import Union, List

from . import enums


ATTRIBUTES = dict(
    list(
        zip(
            [
                "bold",
                "dark",
                "",
                "underline",
                "blink",
                "",
                "reverse",
                "concealed",
            ],
            list(range(1, 9)),
        )
    )
)
del ATTRIBUTES[""]

ATTRIBUTES_RE = "\033\[(?:%s)m" % "|".join(["%d" % v for v in ATTRIBUTES.values()])

HIGHLIGHTS = dict(
    list(
        zip(
            [
                "on_grey",
                "on_red",
                "on_green",
                "on_yellow",
                "on_blue",
                "on_magenta",
                "on_cyan",
                "on_white",
            ],
            list(range(40, 48)),
        )
    )
)

HIGHLIGHTS_RE = "\033\[(?:%s)m" % "|".join(["%d" % v for v in HIGHLIGHTS.values()])

COLORS = dict(
    list(
        zip(
            [
                "grey",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
            ],
            list(range(30, 38)),
        )
    )
)

COLORS_RE = "\033\[(?:%s)m" % "|".join(["%d" % v for v in COLORS.values()])

RESET = "\033[0m"
RESET_RE = "\033\[0m"


def colored(
    text: str,
    color: Union[str, enums.Colors] = None,
    on_color: Union[str, enums.Highlights] = None,
    attrs: Union[List[str], List[enums.Attributes]] = None,
) -> str:
    """Colorize text, while stripping nested ANSI color sequences.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """

    if isinstance(color, enums.Colors):
        color = str(color)

    if isinstance(on_color, enums.Highlights):
        on_color = str(on_color)

    if attrs is not None:
        for i in range(len(attrs)):
            if isinstance(attrs[i], enums.Attributes):
                attrs[i] = str(attrs[i])

    if os.getenv("ANSI_COLORS_DISABLED") is None:
        fmt_str = "\033[%dm%s"
        if color is not None:
            text = re.sub(COLORS_RE + "(.*?)" + RESET_RE, r"\1", text)
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = re.sub(HIGHLIGHTS_RE + "(.*?)" + RESET_RE, r"\1", text)
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            text = re.sub(ATTRIBUTES_RE + "(.*?)" + RESET_RE, r"\1", text)
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        return text + RESET

    else:
        return text


def cprint(
    text: str,
    color: Union[str, enums.Colors] = None,
    on_color: Union[str, enums.Highlights] = None,
    attrs: Union[List[str], List[enums.Attributes]] = None,
    **kwargs
):
    """Print colorize text.

    Also accepts arguments of print function.
    """

    print((colored(text, color, on_color, attrs)), **kwargs)

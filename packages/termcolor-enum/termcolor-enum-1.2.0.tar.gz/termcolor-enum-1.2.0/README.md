# Examples

```python
import sys
from termcolor_enum import *

text = colored('Hello, World!', Colors.RED, attrs=[Attributes.REVERSE, Attributes.BLINK])
print(text)
cprint('Hello, World!', 'green', Highlights.ON_RED)

print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
print_red_on_cyan('Hello, World!')
print_red_on_cyan('Hello, Universe!')

for i in range(10):
    cprint(i, 'magenta', end=' ')

cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)
```

# Text Colors (`termcolor_enum.Colors`):

| Color   | String      | Enum Value |
| ------- | ----------- | ---------- |
| Grey    | `'grey'`    | `GREY`     |
| Red     | `'red'`     | `RED`      |
| Green   | `'green'`   | `GREEN`    |
| Yellow  | `'yellow'`  | `YELLOW`   |
| Blue    | `'blue'`    | `BLUE`     |
| Magenta | `'magenta'` | `MAGENTA`  |
| Cyan    | `'cyan'`    | `CYAN`     |
| White   | `'white'`   | `WHITE`    |

# Text Highlights (`termcolor_enum.Highlights`):

| Highlight  | String         | Enum Value   |
| ---------- | -------------- | ------------ |
| On Grey    | `'on_grey'`    | `ON_GREY`    |
| On Red     | `'on_red'`     | `ON_RED`     |
| On Green   | `'on_green'`   | `ON_GREEN`   |
| On Yellow  | `'on_yellow'`  | `ON_YELLOW`  |
| On Blue    | `'on_blue'`    | `ON_BLUE`    |
| On Magenta | `'on_magenta'` | `ON_MAGENTA` |
| On Cyan    | `'on_cyan'`    | `ON_CYAN`    |
| On White   | `'on_white'`   | `ON_WHITE`   |

# Text Attributes (`termcolor_enum.Attributes`):

| Attribute | String        | Enum Value  |
| --------- | ------------- | ----------- |
| Bold      | `'bold'`      | `BOLD`      |
| Dark      | `'dark'`      | `DARK`      |
| Underline | `'underline'` | `UNDERLINE` |
| Blink     | `'blink'`     | `BLINK`     |
| Reverse   | `'reverse'`   | `REVERSE`   |
| Concealed | `'concealed'` | `CONCEALED` |

# Terminal Compatibility

| Terminal     | Bold    | Dark | Underline | Blink      | Reverse | Concealed |
| ------------ | ------- | ---- | --------- | ---------- | ------- | --------- |
| xterm        | yes     | no   | yes       | bold       | yes     | yes       |
| linux        | yes     | yes  | bold      | yes        | yes     | no        |
| rxvt         | yes     | no   | yes       | bold/black | yes     | no        |
| dtterm       | yes     | yes  | yes       | reverse    | yes     | yes       |
| teraterm     | reverse | no   | yes       | rev/red    | yes     | no        |
| aixterm      | normal  | no   | yes       | no         | yes     | yes       |
| PuTTY        | color   | no   | yes       | no         | yes     | no        |
| Windows      | no      | no   | no        | no         | yes     | no        |
| Cygwin SSH   | yes     | no   | color     | color      | color   | yes       |
| Mac Terminal | yes     | no   | yes       | yes        | yes     | yes       |

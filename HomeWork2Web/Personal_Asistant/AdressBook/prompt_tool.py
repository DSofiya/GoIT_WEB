# from typing import Callable
from prompt_toolkit.document import Document
# from prompt_toolkit.formatted_text.base import StyleAndTextTuples
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLetter(Lexer):
    def lex_document(self, document: Document):
        colors = list(sorted({"Teal": "#008080"}, key=NAMED_COLORS.get))

        def get_line(lineno):
                return [
                    (colors[i % len(colors)], c)
                    for i, c in enumerate(document.lines[lineno])
                ]

        return get_line


Completer = NestedCompleter.from_nested_dict({'hello'   : None, 'add'  : None,
                                              'change': None, 'delete': None, 'search': None,
                                              'show all': None, 'good bye'  : None, 'close' : None,
                                              'exit': None, 'birthday': None})
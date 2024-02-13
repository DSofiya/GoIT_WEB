from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLetter(Lexer):
    def lex_document(self, document):
        colors = list(sorted({"Teal": "#00a28a"}, key=NAMED_COLORS.get))

        def get_line(lineno):
                return [
                    (colors[i % len(colors)], c)
                    for i, c in enumerate(document.lines[lineno])
                ]

        return get_line


Completer = NestedCompleter.from_nested_dict({'add_nuclear'   : None, 'save_nuclear'  : None,
                                              'save_air': None, 'add_air': None, 'save_admin': None,
                                              'add_admin': None,'coordinates': None, 'good bye'  : None,
                                               'close' : None, 'exit': None })
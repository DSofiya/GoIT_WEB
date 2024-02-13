from prompt_toolkit.lexers import Lexer
from prompt_toolkit.styles.named_colors import NAMED_COLORS
from prompt_toolkit.completion import NestedCompleter


class RainbowLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted({"Teal": "#008080"}, key=NAMED_COLORS.get))

        def get_line(lineno):
            return [
                (colors[i % len(colors)], c)
                for i, c in enumerate(document.lines[lineno])
            ]

        return get_line


Completer = NestedCompleter.from_nested_dict({'add_note'   : None, 'edit_note'      : None, 'delete_note': None,
                                            'search_tag'  : None, 'search_content': None, 'display_notes': None,
                                            'edit_note'    : None, 'exit'             : None, 'sort'         : None})

Sort_Completer = NestedCompleter.from_nested_dict({'sort_tags' : None, 'sort_name'  : None, 'sort_date' : None})


     
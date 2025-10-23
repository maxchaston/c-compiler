import dataclasses
import re
from compiler_exceptions import LexException

class Lexer:
    # TODO token_dict

    @staticmethod
    def _largest_regex(text, token_regex_dict) -> re.Match | None:
        matches = []
        for token_type, regex in token_regex_dict.items(): # try all regex matches
            matches.append( (token_type, re.match(regex, text)) )

        matches = list(filter(lambda x: x[1], matches))

        if matches == []: # no regex match found
            return None
        else:
            best_match = max(matches, key=lambda x: len(x[1][0]))
            return best_match
        

    @staticmethod
    def lex(filename: str) -> list[str, re.Match]:
        with open(filename, 'r') as f:
            data = f.read()
            tokens = []
            while len(data) != 0:
                if data[0].encode() in [b' ', b'\t', b'\n', b'\r',b'\x0b', b'\f']:
                    # data=data.lstrip() # remove leading whitespace
                    data=data[1:]
                else:
                    best_match = Lexer._largest_regex(data, Token.regex_dict)
                    if best_match is None: 
                        print("Error: no regex matches found while lexing")
                        print(data[:40])
                        raise LexException()
                    if best_match[0] == 'IDENTIFIER':
                        keyword_match = Lexer._largest_regex(best_match[1][0], Token.keyword_regex_dict)
                        if keyword_match is not None:
                            best_match = keyword_match
                    tokens.append(best_match)
                    data = data[len(best_match[1][0]):]
            return tokens


@dataclasses.dataclass
class Token:
    regex_dict={
        'IDENTIFIER': r'[a-zA-Z_]\w*\b',
        'CONSTANT': r'[0-9]+\b',
        'OPEN_PAREN': r'\(',
        'CLOSE_PAREN': r'\)',
        'OPEN_BRACE': r'\{',
        'CLOSE_BRACE': r'\}',
        'SEMICOLON': r';',
        'TILDE': r'~',
        'HYPHEN': r'-',
        'DECREMENT': r'--',
    }
    keyword_regex_dict={
        'INT_KEYWORD': r'int\b',
        'VOID_KEYWORD': r'void\b',
        'RETURN_KEYWORD': r'return\b',
    }

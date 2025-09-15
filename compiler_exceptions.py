class LexException(Exception):
    """Exception while lexing"""

class ParserException(Exception):
    """Exception while parsing"""

class SyntaxError(ParserException):
    """Unexpected syntax met while parsing"""

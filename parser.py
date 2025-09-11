from dataclasses import dataclass
from lexer import Token
from compiler_exceptions import SyntaxError

# AST classes

@dataclass
class Program:
    function_definition: Function

@dataclass
class Function:
    name: Identifier
    body: Statement

Idenfitifer = str

# will be a union later
Statement = Return

@dataclass
class Return:
    exp: Expression

# will be a union later
Expression = Constant

@dataclass
class Constant:
    val: int


# Main classes
class Parser:
    @staticmethod
    def expect(expected_token, tokens):
        if tokens[0][0] == expected_token:
            del tokens[0]
        else:
            print(f"Incorrect syntax: expected {expected_token} but found {tokens[0][0]}")
            raise SyntaxError
    
    @staticmethod
    def parse_program(tokens):
        return Program(parse_function(tokens))

    @staticmethod
    def parse_function(tokens):
        expect('INT_KEYWORD', tokens)
        func_name = parse_identifier(tokens)
        expect('OPEN_PAREN', tokens)
        expect('VOID_KEYWORD', tokens)
        expect('CLOSE_PAREN', tokens)
        expect('OPEN_PAREN', tokens)
        expect('OPEN_BRACE', tokens)
        func_body = parse_statement(tokens)
        expect('CLOSE_BRACE', tokens)
        return Function(func_name, func_body)

    @staticmethod
    def parse_identifier(tokens):
        if tokens[0][0] == 'IDENTIFIER':
            return Identifier(tokens[0][1][0])
        else:
            print(f"Incorrect syntax: expected IDENTIFIER but found {tokens[0][0]}")
            raise SyntaxError

    @staticmethod
    def parse_statement(tokens):
        expect('RETURN_KEYWORD', tokens)
        exp = parse_expression(tokens)
        expect('SEMICOLON', tokens)
        return Return(exp)

    
    @staticmethod
    def parse_expression(tokens):
        if tokens[0][0] == 'CONSTANT':
            return Constant(int(tokens[0][1][0]))
        else:
            print(f"Incorrect syntax: expected CONSTANT but found {tokens[0][0]}")
            raise SyntaxError

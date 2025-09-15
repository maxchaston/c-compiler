from dataclasses import dataclass
from lexer import Token
from compiler_exceptions import SyntaxError

# AST classes

@dataclass
class Constant:
    val: int

# will be a union later
Expression = Constant

@dataclass
class Return:
    exp: Expression

# will be a union later
Statement = Return

Identifier = str

@dataclass
class Function:
    name: Identifier
    body: Statement

@dataclass
class Program:
    function_definition: Function

# Main classes
class Parser:
    @staticmethod
    def expect(expected_token, tokens):
        print(tokens[0])
        if tokens[0][0] == expected_token:
            del tokens[0]
        else:
            print(f"Incorrect syntax: expected {expected_token} but found {tokens[0][0]}")
            raise SyntaxError
    
    @staticmethod
    def parse_expression(tokens):
        if tokens[0][0] == 'CONSTANT':
            return Constant(int(tokens[0][1][0]))
        else:
            print(f"Incorrect syntax: expected CONSTANT but found {tokens[0][0]}")
            raise SyntaxError

    @staticmethod
    def parse_statement(tokens):
        Parser.expect('RETURN_KEYWORD', tokens)
        exp = Parser.parse_expression(tokens)
        del tokens[0]
        Parser.expect('SEMICOLON', tokens)
        return Return(exp)

    @staticmethod
    def parse_identifier(tokens) -> Identifier:
        if tokens[0][0] == 'IDENTIFIER':
            iden_ret = Identifier(tokens[0][1][0])
            del tokens[0]
            return iden_ret
        else:
            print(f"Incorrect syntax: expected IDENTIFIER but found {tokens[0][0]}")
            raise SyntaxError

    @staticmethod
    def parse_function(tokens) -> Function:
        Parser.expect('INT_KEYWORD', tokens)
        func_name = Parser.parse_identifier(tokens)
        Parser.expect('OPEN_PAREN', tokens)
        Parser.expect('VOID_KEYWORD', tokens)
        Parser.expect('CLOSE_PAREN', tokens)
        Parser.expect('OPEN_BRACE', tokens)
        func_body = Parser.parse_statement(tokens)
        Parser.expect('CLOSE_BRACE', tokens)
        return Function(func_name, func_body)

    @staticmethod
    def parse_program(tokens) -> Program:
        prog_ret = Program(Parser.parse_function(tokens))
        if len(tokens) != 0:
            print(f"Incorrect syntax: unexpected tokens after function")
            raise SyntaxError
        return prog_ret

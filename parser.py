from dataclasses import dataclass
from lexer import Token
from compiler_exceptions import SyntaxError

# AST classes

@dataclass
class Complement:
    ""

@dataclass
class Negate:
    ""

Unary_Op = Complement | Negate

@dataclass
class Unary:
    op: Unary_Op
    exp: 'Expression' # forward reference for type hint

@dataclass
class Constant:
    val: int
    def __str__(self):
        return f"Constant({str(self.val)})"

Expression = Constant | Unary

@dataclass
class Return:
    exp: Expression
    def __str__(self):
        return f"""Return (
        {str(self.exp)}
        )"""

# will be a union later
Statement = Return

Identifier = str

@dataclass
class Function:
    name: Identifier
    body: Statement
    def __str__(self):
        return f"""Function (
  name="{str(self.name)}"
  body={str(self.body)}
)"""

@dataclass
class Program:
    function_definition: Function
    def __str__(self):
        return f"""Program (
  {str(self.function_definition)}
)"""

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
    def parse_unary_operator(tokens):
        match tokens[0][0]:
            case 'TILDE':
                del tokens[0]
                return Complement
            case 'HYPHEN':
                del tokens[0]
                return Negate
            case _:
                print(f"Incorrect syntax: expected valid unary operator but found {tokens[0][0]}")
                raise SyntaxError
    
    @staticmethod
    def parse_expression(tokens):
        match tokens[0][0]:
            case 'CONSTANT':
                val = int(tokens[0][1][0])
                del tokens[0]
                return Constant(val)
            # Unary operators
            case 'TILDE' | 'HYPHEN':
                op = Parser.parse_unary_operator(tokens)
                exp = Parser.parse_expression(tokens)
                return Unary(op, exp)
            case 'OPEN_PAREN':
                Parser.expect('OPEN_PAREN', tokens)
                exp = Parser.parse_expression(tokens)
                Parser.expect('CLOSE_PAREN', tokens)
                return exp
            case _:
                print(f"Incorrect syntax: expected valid expression but found {tokens[0][0]}")
                raise SyntaxError

    @staticmethod
    def parse_statement(tokens):
        Parser.expect('RETURN_KEYWORD', tokens)
        exp = Parser.parse_expression(tokens)
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

    @staticmethod
    def _pretty_print_indent(node, indentation: int):
        leading_space = '  ' * indentation
        def pprint(x):
            print(f"{leading_space}{x}")
        match node:
            case Constant():
                pprint(f"Constant({str(node.val)})")
                return
            case Return():
                pprint(f"Return (")
                Parser._pretty_print_indent(node.exp, indentation+1)
                pprint(f")")
                return 
            case Function():
                pprint(f"Function (")
                pprint(f"{leading_space}name='{node.name}'")
                pprint(f"{leading_space}body=(")
                Parser._pretty_print_indent(node.body, indentation+2)
                pprint(f"{leading_space})")
                pprint(f")")
                return
            case Program():
                pprint(f"Program (")
                Parser._pretty_print_indent(node.function_definition, indentation+1)
                pprint(f")")
                return
                  
                
    @staticmethod
    def pretty_print(node):
        Parser._pretty_print_indent(node, 0)

from dataclasses import dataclass
import parser

@datatclass
class Var:
    name: 'Identifier'

@datatclass
class Constant:
    val: int

Val = Constant | Var

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
    src: Val
    dst: Var

@dataclass
class Return:
    val: Val

Instruction = Return | Unary

Identifier = str

@dataclass
class Function:
    name: Identifier
    body: list[Instruction]

@dataclass
class Program:
    function_definition: Function


class Tacky_Generator:
    # TODO not all there, appending the dst was thrown on and almost certainly isn't what's going to be done but the idea is right
    # Just moving the code over
    @staticmethod
    def parse_expression(expression: parser.Expression) -> list[Instruction]:

    @staticmethod
    def parse_function(function: parser.Function):
        func_name = function.name
        func_instructions = []
        match type(function.body):
            case parser.Return:
               exp_ret = Tacky_generator.parse_expression(function.body.exp)
               func_instructions.append(Return(exp_ret[-1].dst))


        func_ret = Function(func_name, func_instructions)
        return func_ret

    @staticmethod
    def parse_program(program: parser.Program):
        return Program(Tacky_Generator.parse_function(program.function_definition))

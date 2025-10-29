from dataclasses import dataclass
import parser

@dataclass
class Var:
    name: 'Identifier'

@dataclass
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
    tmp_var_func = None
    tmp_var_count = 0

    @staticmethod
    def get_tmp_var_name():
        return str(tmp_var_func) + '.' + str(tmp_var_count)

    @staticmethod
    def convert_parser_unop(unary_op):
        match unary_op:
            case parser.Complement:
                return Complement()
            case parser.Negate:
                return Negate()

    @staticmethod
    def parse_expression(expression: parser.Expression, instructions):
        match expression:
            case parser.Constant:
                return Constant(expression.val)
            case parser.Unary:
                src = Tacky_Generator.parse_expression(expression.exp)
                dst_name = Tacky_Generator.get_tmp_var_name()
                tmp_var_count+=1
                dst = Var(dst_name)
                instructions.append(Unary(convert_parser_unop(expression.op), src, dst))
                
    @staticmethod
    def parse_function(function: parser.Function):
        func_name = function.name
        tmp_var_func = func_name 
        func_instructions = []
        match type(function.body):
            case parser.Return:
                exp_ret = Tacky_Generator.parse_expression(function.body.exp, func_instructions)
                func_instructions.append(Return(Constant(exp_ret)))

        func_ret = Function(func_name, func_instructions)
        return func_ret

    @staticmethod
    def parse_program(program: parser.Program):
        return Program(Tacky_Generator.parse_function(program.function_definition))

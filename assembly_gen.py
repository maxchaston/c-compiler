from dataclasses import dataclass
import parser

# AST classes

@dataclass
class Imm:
    val: int

@dataclass
class Register:
    ""

Operand = Imm | Register

@dataclass
class Mov:
    src: Operand
    dst: Operand

@dataclass
class Ret:
    ""

Instruction = Mov | Ret

Identifier = str

@dataclass
class Function:
    name: Identifier
    instructions: list[Instruction]

@dataclass
class Program:
    function_definition: Function


# Main classes

class Assembly_Generator:
    @staticmethod
    def parse_expression(exp: parser.Expression):
        match exp:
            case Constant:
                return Imm(exp.val)

    @staticmethod
    def parse_function(function: parser.Function):
        func_instructions = []
        match type(function.body):
            case parser.Return:
                ret_exp = Assembly_Generator.parse_expression(function.body.exp)
                ret_mov = Mov(ret_exp, Register())
                func_instructions = [ret_mov, Ret()]
                
        func_ret = Function(function.name, func_instructions)
        return func_ret

    @staticmethod
    def parse_program(program: parser.Program):
        prog_ret = Program(Assembly_Generator.parse_function(program.function_definition))
        return prog_ret

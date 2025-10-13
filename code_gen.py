import assembly_gen as ag

class Code_Generator:

    assembly_code = []

    @staticmethod
    def format_operand(operand: ag.Operand):
        match operand:
            case ag.Register():
                return '%eax'
            case ag.Imm():
                return f'${operand.val}'
                       
    @staticmethod
    def format_instruction(instruction: ag.Instruction):
        match instruction:
            case ag.Mov():
                return f'movl {Code_Generator.format_operand(instruction.src)}, {Code_Generator.format_operand(instruction.dst)}'
            case ag.Ret():
                return 'ret'

    @staticmethod
    def gen_function(function: ag.Function):
        Code_Generator.assembly_code.append(f'\t.globl {function.name}')
        Code_Generator.assembly_code.append(f'{function.name}:')
        for instruction in function.instructions:
            Code_Generator.assembly_code.append(f'\t{Code_Generator.format_instruction(instruction)}')

    @staticmethod
    def gen_program(program: ag.Program):
        _header = '''.section .note.GNU-stack,"",@progbits''' # no executable stack
        Code_Generator.gen_function(program.function_definition)
        Code_Generator.assembly_code.append(f'\t{_header}')
        return Code_Generator.assembly_code
        

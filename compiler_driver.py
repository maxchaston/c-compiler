#!/usr/bin/env python 

import subprocess
from assembly_gen import Assembly_Generator
from tacky_gen import Tacky_Generator
from code_gen import Code_Generator
from lexer import Lexer
from parser import Parser
import argparse
import re

class CompilerDriver:
    filename=''
    filename_root=''
    @staticmethod
    def preprocess(filename: str):
        print("Preprocessing...",end='\r')
        command_to_run = f'gcc -E -P {filename} -o {CompilerDriver.filename_root + ".i"}' # -E to only run preprocessor, -P do not emit line markers
        completed_process = subprocess.run(command_to_run.split(' '))
        if completed_process.returncode != 0:
            print(f"Error occured while running preprocessor: {completed_process.stderr}")
        else:
            print(f"Preprocess completed successfully")

    @staticmethod
    def lex(filename: str) -> list[str]:
        print("Lexing...",end='\r')
        lex_ret = Lexer.lex(filename)
        print("Lexing completed successfully")
        return lex_ret

    @staticmethod
    def parse(tokens: list[str]):
        print("Parsing...",end='\r')
        parse_ret = Parser.parse_program(tokens)
        print("Parsing completed successfully")
        return parse_ret

    @staticmethod
    def tacky_gen(parse_program):
        print("Generating TACKY...", end='\r')
        tacky_gen_ret = Tacky_Generator.parse_program(parse_program)
        print("TACKY generation completed successfully\n")
        print(tacky_gen_ret, end='\n\n')
        return tacky_gen_ret

    @staticmethod
    def assembly_gen(parse_program):
        print("Generating assembly...", end='\r')
        assembly_gen_ret = Assembly_Generator.parse_program(parse_program)
        print("Assembly generation completed successfully\n")
        print(assembly_gen_ret, end='\n\n')
        return assembly_gen_ret

    @staticmethod
    def code_gen(ass_program):
        print("Generating code...", end='\r')
        code_gen_ret = Code_Generator.gen_program(ass_program)
        print("Code generation completed successfully\n")
        print(*code_gen_ret, sep='\n', end='\n\n')
        return code_gen_ret

    @staticmethod
    def write_assembly_file(code_arr):
        print(f'Writing assembly file to {CompilerDriver.filename_root}.s')
        with open(f'{CompilerDriver.filename_root}.s', 'w') as f:
            code = '\n'.join(code_arr)
            code+='\n'
            f.write(code)

    @staticmethod
    def run_assembler():
        command_to_run = f'gcc -c {CompilerDriver.filename_root + ".s"} -o {CompilerDriver.filename_root + ".o"}'
        completed_process = subprocess.run(command_to_run.split(' '))
        if completed_process.returncode != 0:
            print(f"Error occured while running assembler: {completed_process.stderr}")
        else:
            print(f"Assembler completed successfully")

    @staticmethod
    def run_linker():
        command_to_run = f"gcc {CompilerDriver.filename_root}.o -o {CompilerDriver.filename_root}"
        completed_process = subprocess.run(command_to_run.split(' '))
        if completed_process.returncode != 0:
            print(f"Error occured while running linker: {completed_process.stderr}")
        else:
            print(f"Linker completed successfully")

def main():
    parser = argparse.ArgumentParser(prog='c compiler driver')
    parser.add_argument('filename')
    parser.add_argument('--lex', action='store_true') # run lexer, but stop before parsing
    parser.add_argument('--parse', action='store_true') # run lexer and parser, but stop before assembly gen
    parser.add_argument('--codegen', action='store_true') # run lexer, parser and assembly gen, but stop before code emission
    parser.add_argument('-S', action='store_true') # emit an assembly file

    args = parser.parse_args()

    CompilerDriver.filename = args.filename
    print(f'Got filename: {CompilerDriver.filename}')
    CompilerDriver.filename_root = CompilerDriver.filename.split('.')[0] # assuming in format of root.c
    print(f'Got filename root: {CompilerDriver.filename_root}')

    # preprocess
    CompilerDriver.preprocess(CompilerDriver.filename)

    # lex
    lex_ret = CompilerDriver.lex(CompilerDriver.filename_root+'.i')
    if args.lex:
        return

    # parse
    parse_ret = CompilerDriver.parse(lex_ret)
    Parser.pretty_print(parse_ret)
    if args.parse:
        return

    # codegen:
    assembly_gen_ret = CompilerDriver.assembly_gen(parse_ret)
    code_gen_ret = CompilerDriver.code_gen(assembly_gen_ret)
    CompilerDriver.write_assembly_file(code_gen_ret)
    CompilerDriver.run_assembler()
    CompilerDriver.run_linker()

if __name__ == "__main__":
    main()

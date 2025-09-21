#!/usr/bin/env python 

import subprocess
from assembly_gen import Assembly_Generator 
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
        command_to_run = f'gcc -E -P {filename} -o {CompilerDriver.filename_root + '.i'}' # -E to only run preprocessor, -P do not emit line markers
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
    def assembly_gen(program):
        print("Generating assembly...", end='\r')
        assembly_gen_ret = Assembly_Generator.parse_program(program)
        print("Assembly generation completed successfully")
        print(assembly_gen_ret)
        return assembly_gen_ret

def main():
    parser = argparse.ArgumentParser(prog='c compiler driver')
    parser.add_argument('filename')
    parser.add_argument('--lex', action='store_true') # run lexer, but stop before parsing
    parser.add_argument('--parse', action='store_true') # run lexer and parser, but stop before assembly gen
    parser.add_argument('--codegen', action='store_true') # run lexer, parser and assembly gen, but stop before code emission
    parser.add_argument('-S', action='store_true') # emit an assembly file

    args = parser.parse_args()

    CompilerDriver.filename = args.filename
    CompilerDriver.filename_root = CompilerDriver.filename.split('.')[0] # assuming in format of root.c

    # preprocess
    CompilerDriver.preprocess(CompilerDriver.filename)

    # lex
    if args.lex or args.parse or args.codegen:
        lex_ret = CompilerDriver.lex(CompilerDriver.filename_root+'.i')

        # parse
        if args.parse or args.codegen:
            parse_ret = CompilerDriver.parse(lex_ret)
            Parser.pretty_print(parse_ret)

            if args.codegen:
                assembly_gen_ret = CompilerDriver.assembly_gen(parse_ret)

if __name__ == "__main__":
    main()

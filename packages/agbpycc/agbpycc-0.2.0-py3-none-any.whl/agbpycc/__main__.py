import argparse
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import List, Optional

from .parse_debug import process_debug_info
from .parser import parse, generate_ast, apply_transformations, ASTDump


class Stage(IntEnum):
    PREPROCESS = auto()
    COMPILE = auto()
    ASSEMBLE = auto()
    LINK = auto()


def get_next_stage_for_filename(filename: str) -> Stage:
    if filename.endswith('.c'):
        return Stage.PREPROCESS
    if filename.endswith('.i'):
        return Stage.COMPILE
    if filename.endswith('.s'):
        return Stage.ASSEMBLE
    if filename.endswith('.o'):
        return Stage.LINK
    logging.error(f'{filename} does not end with a recognized extension, could not determine starting stage')
    exit(1)


@dataclass
class CompilerOptions:
    include_directories: List[str]
    quote_include_directories: List[str]
    cc1_binary: str
    preproc_binary: str
    preproc_charmap: str
    warnings: List[str]
    optimizations: int
    input_filename: str
    output_filename: str
    debug: bool
    no_parse: str
    starting_stage: Stage
    current_stage: Stage
    target_stage: Stage

    def advance_stage(self):
        self.current_stage = Stage(self.current_stage + 1)


def print_version(args: Optional[List[str]]):
    print('agbpycc version TODO')
    for arg in args:
        git_proc = subprocess.run(['git', '--git-dir=' + arg + '/.git', 'rev-parse', '--short', 'HEAD'],
                                  stdout=subprocess.PIPE)
        print(f'{os.path.basename(arg)}@{git_proc.stdout.decode("utf-8").strip()}')


def parse_args(argv: List[str]) -> CompilerOptions:
    parser = argparse.ArgumentParser(description='compiler frontend for agbcc')
    parser.add_argument('--version', nargs='*')
    parser.add_argument('-I', action='append', help='add include paths')
    parser.add_argument('-iquote', action='append', help='add quote include paths')
    parser.add_argument('--cc1', help='path to agbcc binary')
    parser.add_argument('--preproc', help='preproc path')
    parser.add_argument('--charmap', help='preproc charmap')
    parser.add_argument('-E', action='store_const', help='preprocess only', dest='stage',
                        const=Stage.PREPROCESS)
    parser.add_argument('-S', action='store_const', help='output assembly (default)', dest='stage',
                        const=Stage.COMPILE)
    parser.add_argument('-c', action='store_const', help='output object (unsupported)', dest='stage',
                        const=Stage.ASSEMBLE)
    parser.add_argument('-W', action='append', help='enable warnings')
    parser.add_argument('-O', nargs='?', help='set optimization level', default=0, const=1)
    parser.add_argument('input', help='input filename', nargs='?')
    parser.add_argument('-o', help='output file name')
    parser.add_argument('-g', help='output debug information', action='store_true', dest='debug')
    parser.add_argument('-nog', help='do not output debug information (debug option)', action='store_false',
                        dest='debug')
    parser.add_argument('--no-parse', action='store_true', help='disable processing of assembly code (debug option)')
    parser.add_argument('--log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='WARNING',
                        help='choose log level, default WARNING')

    args = parser.parse_args(argv)

    if args.version is not None:
        print_version(args.version)
        exit(0)

    loglevel = args.log
    numeric_level = getattr(logging, loglevel.upper(), None)
    logging.basicConfig(format='agbpycc:%(levelname)s: %(message)s', level=numeric_level)

    if not args.input:
        logging.error('no input file provided')
        exit(1)

    options = CompilerOptions(
        include_directories=args.I or [],
        quote_include_directories=args.iquote or [],
        cc1_binary=args.cc1,
        preproc_binary=args.preproc,
        preproc_charmap=args.charmap,
        warnings=args.W or [],
        optimizations=args.O,
        input_filename=args.input,
        output_filename=args.o,
        debug=args.debug,
        no_parse=args.no_parse,
        starting_stage=get_next_stage_for_filename(args.input),
        current_stage=get_next_stage_for_filename(args.input),
        target_stage=args.stage or Stage.COMPILE,
    )

    if options.starting_stage <= Stage.COMPILE <= options.target_stage:
        if not options.cc1_binary:
            logging.error('cc1/agbcc is required for compiling code')
            exit(1)

    return options


def get_source_filename_for_stage(options: CompilerOptions) -> str:
    if options.current_stage is options.starting_stage:
        return options.input_filename
    if options.current_stage is Stage.PREPROCESS:
        return f'{options.input_filename}.c'
    if options.current_stage is Stage.COMPILE:
        return f'{options.input_filename}.i'
    if options.current_stage is Stage.ASSEMBLE:
        return f'{options.input_filename}.s'
    if options.current_stage is Stage.LINK:
        return f'{options.input_filename}.o'
    logging.error('bad stage, this is an error in agbpycc')
    logging.debug(f'stage {options.current_stage} in get_source_filename_for_stage')
    exit(1)


def get_target_filename_for_stage(options: CompilerOptions) -> str:
    if options.current_stage is options.target_stage and options.output_filename:
        return options.output_filename
    if options.current_stage is Stage.PREPROCESS:
        return f'{options.input_filename}.i'
    if options.current_stage is Stage.COMPILE:
        return f'{options.input_filename}.s'
    if options.current_stage is Stage.ASSEMBLE:
        return f'{options.input_filename}.o'
    if options.current_stage is Stage.LINK:
        return f'a.out'
    logging.error('bad stage, this is an error in agbpycc')
    logging.debug(f'stage {options.current_stage} in get_target_filename_for_stage')
    exit(1)


def do_preprocess(options: CompilerOptions):
    cpp_args = ['cpp', '-nostdinc', '-undef']

    for q in options.quote_include_directories:
        cpp_args += ['-iquote', q]

    for b in options.include_directories:
        cpp_args += ['-I', b]

    source = get_source_filename_for_stage(options)
    target = get_target_filename_for_stage(options)

    cpp_args += [source, '-o', target]
    subprocess.call(cpp_args)
    # TODO move preproc here?


def do_compile(options: CompilerOptions):
    source = get_source_filename_for_stage(options)
    target = get_target_filename_for_stage(options)

    cc1 = [options.cc1_binary, '-fhex-asm', '-o', target]
    if options.debug:
        cc1.append('-g')
    if options.optimizations:
        cc1.append(f'-O{options.optimizations}')
    for warning in options.warnings:
        cc1.append(f'-W{warning}')

    # TODO move preproc into preprocess step
    if options.preproc_binary and options.preproc_charmap:
        pprocess = subprocess.Popen([options.preproc_binary, source, options.preproc_charmap], stdout=subprocess.PIPE)
        subprocess.call(cc1, stdin=pprocess.stdout)
    else:
        with open(source, 'r') as a:
            subprocess.call(cc1, stdin=a)


def process_asm(options: CompilerOptions):
    asm_file = get_target_filename_for_stage(options)
    try:
        if options.debug:
            process_debug_info(asm_file)
        tree, success = parse(asm_file)
        if not success:
            raise ValueError('could not parse file')
        ast = generate_ast(tree)
        apply_transformations(ast)
        with open(asm_file, 'w') as destination_file:
            ASTDump(destination_file).visit(ast)
    except Exception as e:
        logging.warning(f'error cleaning assembly code: {e}\nOutputting unprocessed assembly')


def cleanup(options: CompilerOptions):
    # TODO this needs more elaborate detection of intermediate files
    for file in [f'{options.input_filename}.i']:
        if os.path.exists(file):
            os.remove(file)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    status_code = 0
    options = parse_args(argv)
    try:
        # special case for just cleaning assembly code
        if options.current_stage is Stage.ASSEMBLE and options.target_stage is Stage.COMPILE:
            options.current_stage = Stage.COMPILE
            shutil.copyfile(options.input_filename, options.output_filename)
            if not options.no_parse:
                process_asm(options)
            exit(0)
        if options.current_stage is Stage.PREPROCESS and options.current_stage <= options.target_stage:
            do_preprocess(options)
            options.advance_stage()
        if options.current_stage is Stage.COMPILE and options.current_stage <= options.target_stage:
            do_compile(options)
            if options.target_stage is Stage.COMPILE and not options.no_parse:
                process_asm(options)
            options.advance_stage()
        if options.current_stage is Stage.ASSEMBLE and options.current_stage <= options.target_stage:
            options.advance_stage()
            logging.error('assembling code not supported yet')
            status_code = 1
        if options.current_stage is Stage.LINK and options.current_stage <= options.target_stage:
            logging.error('linking not supported')
            status_code = 1
    finally:
        cleanup(options)
    exit(status_code)


if __name__ == '__main__':
    main()

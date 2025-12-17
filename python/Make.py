#!/usr/bin/env python3
# @file      Make.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023-2025, Sergey Baigudin, Baigudin Software

import sys
import time
import argparse

from common.System import System
from common.Message import Message
from make.ProgramOnPosix import ProgramOnPosix
from make.ProgramOnWin32 import ProgramOnWin32
from make.ProgramOnBaremetal import ProgramOnBaremetal

class Make:
    """
    Make program.
    """

    def __init__(self):
        self.__args = None


    def build(self):
        """
        Builds EOOS system.
        """
        time_start = time.time()
        res = True
        try:
            Message.out(f'Welcome to {self.__PROGRAM_NAME}', Message.OK, True)
            self.__parse_args()
            self.__print_args()
            program = None
            if self.__get_args().eoos == f'POSIX':
                program = ProgramOnPosix( self.__get_args() )
            elif self.__get_args().eoos == f'WIN32':
                program = ProgramOnWin32( self.__get_args() )
            elif self.__get_args().eoos == f'Generic' or self.__get_args().eoos == f'FreeRTOS':
                program = ProgramOnBaremetal( self.__get_args() )
            else:
                raise Exception(f'EOOS project not supported')
            if program is not None:
                program.execute()
            else:
                raise Exception(f'Program is not set')
        except Exception as e:
            Message.out(f'[EXCEPTION] {e}', Message.ERR)
            res = False
        finally:
            status = Message.OK
            not_word = ''
            if res == False:
                status = Message.ERR
                not_word = ' NOT'
            time_execute = round(time.time() - time_start, 9)
            Message.out(f'{self.__PROGRAM_NAME} has{not_word} been completed in {str(time_execute)} seconds', status, is_block=True)
            return res


    def __get_args(self):
        return self.__args


    def __parse_args(self):
        parser = argparse.ArgumentParser(prog=self.__PROGRAM_NAME \
            , description='Builds and installs the EOOS project to your host OS, or HW platform' \
            , epilog='(c) 2023-2025, Sergey Baigudin, Baigudin Software' \
        )
        parser.add_argument('-e', '--eoos' \
            , choices=['POSIX', 'WIN32', 'FreeRTOS', 'Generic'] \
            , help='select a target EOOS project' \
            , required=True \
        )
        parser.add_argument('-c', '--clean' \
            , action='store_true' \
            , help='rebuild the project by removing the `build` directory artifacts' \
        )
        parser.add_argument('-b', '--build' \
            , choices=['EOOS', 'ALL'] \
            , help='compile either EOOS library target, or all targets' \
        )
        parser.add_argument('-r', '--run' \
            , metavar='GTEST_FILTER_PATTERN' \
            , nargs='*' \
            , help='filter unit tests' \
        )
        parser.add_argument('--coverage' \
            , action='store_true' \
            , help='run unit tests and create code coverage report' \
        )
        parser.add_argument('--install' \
            , action='store_true' \
            , help='install on host OS' \
        )
        parser.add_argument('--config' \
            , choices=['Release', 'Debug', 'RelWithDebInfo', 'MinSizeRel'] \
            , default='Debug' \
            , help='set project configuration' \
        )
        parser.add_argument('--toolchain' \
            , help='define CMake toolchain file name in `cmake` direcrory' \
        )
        parser.add_argument('-j', '--jobs' \
            , type=int \
            , help='set number of parallel jobs to build' \
        )
        parser.add_argument('--verbose' \
            , action='store_true' \
            , help='verbose compiler output' \
        )
        parser.add_argument('-d', '--define' \
            , metavar='DEFINITIONS' \
            , nargs='*' \
            , help='create or update a CMake cache entry in DEFINITIONS format <var>:<type>=<value>, or <var>=<value>' \
        )
        parser.add_argument('--version' \
            , action='version' \
            , version=f'%(prog)s {self.__PROGRAM_VERSION}' \
        )
        self.__args = parser.parse_args()


    def __print_args(self):
        if self.__get_args().eoos is not None:
            Message.out(f'[INFO] Argument EOOS: {self.__get_args().eoos}', Message.INF)
        if self.__get_args().clean is True:
            Message.out(f'[INFO] Argument CLEAN: {self.__get_args().clean}', Message.INF)
        if self.__get_args().build is not None:
            Message.out(f'[INFO] Argument BUILD: {self.__get_args().build}', Message.INF)
        if self.__get_args().run is not None:
            Message.out(f'[INFO] Argument RUN: PASSED', Message.INF)
            for i, d in enumerate(self.__get_args().run):
                Message.out(f'[INFO] Argument RUN {i}: {d}', Message.INF)
        if self.__get_args().coverage is True:
            Message.out(f'[INFO] Argument COVERAGE: {self.__get_args().coverage}', Message.INF)
        if self.__get_args().install is True:
            Message.out(f'[INFO] Argument INSTALL: {self.__get_args().install}', Message.INF)
        if self.__get_args().config is not None:
            Message.out(f'[INFO] Argument CONFIG: {self.__get_args().config}', Message.INF)
        if self.__get_args().toolchain is not None:
            Message.out(f'[INFO] Argument TOOLCHAIN: {self.__get_args().toolchain}', Message.INF)
        if self.__get_args().jobs is not None:
            Message.out(f'[INFO] Argument JOBS: {self.__get_args().jobs}', Message.INF)
        if self.__get_args().verbose is True:
            Message.out(f'[INFO] Argument VERBOSE: {self.__get_args().verbose}', Message.INF)
        if self.__get_args().define is not None:
            Message.out(f'[INFO] Argument DEFINE: PASSED', Message.INF)
            for i, d in enumerate(self.__get_args().define):
                Message.out(f'[INFO] Argument DEFINE {i}: {d}', Message.INF)
        if self.__get_args().install is True:
            Message.out(f'[NOTE] To install EOOS on Windows, a console has to be run as Administrator.', Message.NOR)


    __PROGRAM_NAME = 'EOOS Safe Project Builder'
    __PROGRAM_VERSION = '2.2.0'


def main():
    if Make().build() is True:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit( main() )

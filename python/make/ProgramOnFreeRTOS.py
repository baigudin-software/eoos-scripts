#!/usr/bin/env python3
# @file      ProgramOnFreeRTOS.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2024-2025, Sergey Baigudin, Baigudin Software

import os.path

from make.Program import Program
from common.System import System
from common.Message import Message

class ProgramOnFreeRTOS(Program):
    """
    Program on ProgramOnFreeRTOS.
    """

    def __init__(self, args):
        super().__init__(args)


    def _do_build(self):
        if self._get_args().build is not None:
            if self._get_args().toolchain is None:
                Message.out(f'[WARNING] Toolchain file is not passed', Message.ERR)
            else:
                if os.path.isfile(f'./../../cmake/{self._get_args().toolchain}') is not True:
                    raise Exception(f'Toolchain file does not exist')
            if System.is_linux():
                self.__do_build_on_linux()
            elif System.is_win32():
                self.__do_build_on_win32()
            else:
                raise Exception(f'Unknown host OS')


    def _do_install(self):
        if self._get_args().install is True:
            raise Exception(f'EOOS FreeRTOS program cannot be installed as the feature is in development')


    def _do_run(self):
        if self._get_args().run is not None:
            raise Exception(f'EOOS FreeRTOS program cannot be run as the feature is in development')


    def _do_coverage(self):
        if self._get_args().coverage is True:
            raise Exception(f'EOOS FreeRTOS program cannot be covered as the feature is in development')


    def _get_run_ut_executable_path_to(self):
        return f'./codebase/tests'


    def _get_run_ut_executable_path_back(self):
        return './../..'


    def _get_run_executable(self):
        return f'./EoosTests.elf'


    def __do_build_on_linux(self):
        if self._get_args().build is None:
            return

        args = ['cmake', \
                f'-DCMAKE_BUILD_TYPE={self._get_args().config}' \
        ]
        if self._get_args().toolchain is not None:
            args.append(f'-DCMAKE_TOOLCHAIN_FILE=./../cmake/{self._get_args().toolchain}')
        if self._get_args().build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
        elif self._get_args().build == 'EOOS':
            raise Exception(f'The EOOS parameter of --build argument is not processed for the moment')
        else:
            raise Exception(f'Cannot process --build {self._get_args().build} argument')

        if self._get_args().define is not None:
            for d in self._get_args().define:
                args.append(f'-D{d}')
        args.append('..')
        self._run_subprocess_from_build_dir(args)

        args.clear()
        args = ['make', 'all']
        if self._get_args().verbose is True:
            args.append('VERBOSE=1')
        if self._get_args().jobs is not None:
            args.extend(['-j', str(self._get_args().jobs)])
        Message.out(f'[BUILD] Building Make project...', Message.INF)
        self._run_subprocess_from_build_dir(args)


    def __do_build_on_win32(self):
        if self._get_args().build is None:
            return

        args = ['cmake', \
                '-GMinGW Makefiles', \
                f'-DCMAKE_BUILD_TYPE={self._get_args().config}' \
        ]
        if self._get_args().toolchain is not None:
            args.append(f'-DCMAKE_TOOLCHAIN_FILE=./../cmake/{self._get_args().toolchain}')
        if self._get_args().build == 'ALL':
            Message.out(f'[BUILD] Generating CMake project for all targets...', Message.INF)
        elif self._get_args().build == 'EOOS':
            raise Exception(f'The EOOS parameter of --build argument is not processed for the moment')
        else:
            raise Exception(f'Cannot process --build {self._get_args().build} argument')
        if self._get_args().define is not None:
            for d in self._get_args().define:
                args.append(f'-D{d}')
        args.append('..')
        self._run_subprocess_from_build_dir(args)

        args.clear()
        Message.out(f'[BUILD] Building CMake project...', Message.INF)
        args = ['cmake', '--build', '.', '--config', self._get_args().config]
        if self._get_args().verbose is True:
            args.append('--verbose')
        if self._get_args().jobs is not None:
            args.extend(['-j', str(self._get_args().jobs)])
        self._run_subprocess_from_build_dir(args)

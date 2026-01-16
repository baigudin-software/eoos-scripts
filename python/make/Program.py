#!/usr/bin/env python3
# @file      Program.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023-2026, Sergey Baigudin, Baigudin Software

import os
import shutil
import subprocess

from abc import ABC, abstractmethod
from common.IProgram import IProgram
from common.Message import Message

class Program(IProgram):
    """
    Abstatact base program.
    """

    def __init__(self, args):
        self.__args = args


    def execute(self):
        self.__check_run_path()
        self.__do_clean()
        self.__do_create()
        self._do_build()
        self._do_install()
        self._do_run()
        self._do_coverage()


    @abstractmethod
    def _do_build(self):
        """
        Builds EOOS system.
        """
        pass


    @abstractmethod
    def _do_install(self):
        """
        Installs EOOS system.
        """
        pass


    @abstractmethod
    def _do_run(self):
        """
        Run EOOS program on a target.
        """
        pass


    @abstractmethod
    def _do_coverage(self):
        """
        Creates EOOS UT code coverage report.
        """
        pass


    @abstractmethod
    def _get_run_ut_executable_path_to(self):
        """
        Returns path to EOOS UT executable file.
        """
        pass


    @abstractmethod
    def _get_run_ut_executable_path_back(self):
        """
        Returns path back from EOOS UT executable file.
        """
        pass


    @abstractmethod
    def _get_run_executable(self):
        """
        Returns UT executablr file name.
        """
        pass


    def _run_subprocess_from_build_dir(self, args, path_to=None, path_back=None):
        """
        Runs a sub-process with given args changing current working directory.
        """
        if path_to is None:
            path_to = self._PATH_TO_BUILD_DIR
        if path_back is None:
            path_back = self._PATH_TO_SCRIPT_DIR
        os.chdir(path_to)
        ret = subprocess.run(args).returncode
        os.chdir(path_back)
        if ret != 0:
            raise Exception(f'Execution aborted with return code [{ret}]')


    def _get_args(self):
        """
        Returns program arguments.
        """
        return self.__args


    def _do_run_ut(self):
        if self._get_args().run is None:
            return
        Message.out(f'[BUILD] Running unit tests...', Message.INF)
        args = [self._get_run_executable()]
        if self._get_args().noshuffle is not True:
            args.append('--gtest_shuffle')
        if len(self._get_args().run) > 0:
            arg = '--gtest_filter='
            if self._get_args().run is not None:
                for i, r in enumerate(self._get_args().run):
                    arg += r
                    if i != len(self._get_args().run) - 1:
                        arg += ':'
            args.append(arg)
        path_to = f'{self._PATH_TO_BUILD_DIR}/{ self._get_run_ut_executable_path_to()}'
        path_back = f'{self._get_run_ut_executable_path_back()}/{self._PATH_TO_SCRIPT_DIR}'
        self._run_subprocess_from_build_dir(args, path_to, path_back)


    def __do_clean(self):
        if self._get_args().clean is not True:
            return
        if os.path.isdir(self._PATH_TO_BUILD_DIR):
            Message.out(f'[BUILD] Deleting "build" directory...', Message.INF)
            shutil.rmtree(self._PATH_TO_BUILD_DIR)


    def __do_create(self):
        if not os.path.exists(self._PATH_TO_BUILD_DIR):
            Message.out(f'[BUILD] Creating "build" directory...', Message.INF)
            os.makedirs(self._PATH_TO_BUILD_DIR)
            os.makedirs(self._PATH_TO_BUILD_DIR + '/CMakeInstallDir')
            os.makedirs(self._PATH_TO_BUILD_DIR + '/sca')


    def __check_run_path(self):
        if self.__is_correct_location() is not True:
            raise Exception(f'Script run directory is wrong. Please, run it from "\scripts\python\" directory')


    def __is_correct_location(self):
        if os.path.isdir(f'./../python') is not True:
            return False
        if os.path.isdir(f'./../../scripts') is not True:
            return False
        if os.path.isdir(f'./../../codebase') is not True:
            return False
        return True


    _PATH_TO_BUILD_DIR = './../../build'
    _PATH_TO_SCRIPT_DIR = './../scripts/python'

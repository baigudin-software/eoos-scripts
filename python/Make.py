#!/usr/bin/env python3
# @file      Make.py
# @author    Sergey Baigudin, sergey@baigudin.software
# @copyright 2023, Sergey Baigudin, Baigudin Software

import sys
from make.Program import Program


def main():
    try:
        program = Program()
        return program.execute()
    except BaseException as e:
        print(e)    
        return 1


if __name__ == "__main__":
    sys.exit( main() )

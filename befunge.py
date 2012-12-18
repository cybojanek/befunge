#!/usr/bin/env python
import sys
import argparse

from befunge.BefungeProgram import BefungeProgram

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Befunge Interpreter')
    parser.add_argument('file', help='Befunge program file')
    parser.add_argument('-s', '--steps', action='store_true', help='Show program steps')
    parser.add_argument('-o', '--ops', type=int, help='operations/second', default=0)
    args = parser.parse_args()
    p = BefungeProgram(name=args.file,show_steps=args.steps,operations_per_second=args.ops)
    p.run()

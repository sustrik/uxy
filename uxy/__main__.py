#!/usr/bin/env python3

#  Copyright (c) 2019 Martin Sustrik
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom
#  the Software is furnished to do so, subject to the following conditions:
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
import argparse
import importlib
import sys

def main():

  # Start by finding the subcommand and splitting args meant for __main__.py itself and
  # the arguments to be passed to the subcommand (which may be an arbitrary
  # UNIX tool with arbitrary arguments).
  idx = len(sys.argv)
  for i in range(1, len(sys.argv)):
    if not sys.argv[i].startswith("-"):
      idx = i
      break

  parser = argparse.ArgumentParser(prog="__main__.py",
    description="Tool to manipulate UXY data.")
  parser.add_argument('-l', '--long', action="store_true", default=False,
    help = "print out all available data")
  parser.add_argument('--test', action="store_true", default=False,
    help = "get input from stdin rather than running the wrapped tool; " +
           "used for testing")
  parser.add_argument('--platform', default=sys.platform,
    help = "force a specific platform behaviour; used for testing")
  parser.add_argument('subcommand', metavar="SUBCOMMAND",
    help = "subcommand to execute")
  uxy_args = parser.parse_args(sys.argv[1:idx + 1])
  subcommand = sys.argv[idx].replace("-", "_")
  args = sys.argv[idx:]

  try:
    module = importlib.import_module("uxy.uxy_" + subcommand)
  except:
    print("__main__.py: invalid subcommand '%s'" % subcommand, file=sys.stderr)
    sys.exit(1)

  returncode = getattr(module, subcommand)(args, uxy_args)
  sys.exit(returncode)

if __name__ == "__main__":
    main()

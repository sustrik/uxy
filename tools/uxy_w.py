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
import re
import sys

from tools import base

def _linux_args(args):
  parser = argparse.ArgumentParser("uxy w", add_help=False)
  parser.add_argument("-h", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--no-header", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-s", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--short", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-f", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--from", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-o", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--old-style", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--help", action="store_true", default=argparse.SUPPRESS)
  base.check_args(args, parser)
  return args + []

def _osx_args(args):
  return args + []

def _bsd_args(args):
  return args + []

def w(parser, args, uxy_args):
  # Launch the underlying binary.
  if uxy_args.platform.startswith("linux"):
    args = _linux_args(args)
  elif uxy_args.platform.startswith("darwin"):
    args = _osx_args(args)
  else:
    args = _bsd_args(args)
  proc = base.launch(uxy_args, ['w'] + args[1:])
  # Ignore status line.
  proc.readline()
  # Process the header line.
  hdr = proc.readline()
  parser = base.FmtParser(hdr)
  fmt = base.Format(hdr)
  base.writeline(fmt.render())
  # Process data lines.
  for ln in proc:
    base.writeline(fmt.render(parser.extract(ln)))
  return proc.wait()


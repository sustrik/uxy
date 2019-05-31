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

def _linux(parser, args, uxy_args):
  parser = argparse.ArgumentParser("uxy ps", add_help=False)
  parser.add_argument("-c", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--context", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-f", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-F", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-j", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-l", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-M", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-o", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-O", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-y", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--cols", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--columns", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--forest", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-H", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--headers", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--lines", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--no-headers", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--rows", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--width", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--help", nargs=1, default=argparse.SUPPRESS)
  base.check_args(args, parser)

  # TODO: This is better parsed as fixed-width fields.
  if uxy_args.long:
    fmtargs = ['-FMlww', '--no-headers']
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = base.Format("CONTEXT        F  S  UID        PID    PPID    C  PRI  NI  ADDR  SZ        WCHAN    RSS     PSR  STIME   TTY    TIME       CMD")
  else:
    fmtargs = ['-ww', '--no-headers']
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = base.Format("PID      TTY      TIME       CMD")

  proc = base.launch(uxy_args, ['ps'] + fmtargs + args[1:])
  base.writeline(fmt.render())
  for ln in proc:
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups + 1):
      fields.append(base.encode_field(m.group(i)))
    base.writeline(fmt.render(fields))

def _bsd(parser, args, uxy_args):
  # TODO
  pass

def ps(parser, args, uxy_args):
  if sys.platform.startswith("linux"):
    _linux(parser, args, uxy_args)
  else:
    _bsd(parser, args, uxy_args)

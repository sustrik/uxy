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

import base

def du(parser, args, uxy_args):
  parser = argparse.ArgumentParser("uxy du", add_help=False)
  parser.add_argument("-0", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--null", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-c", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--total", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-h", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--human-readable", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--si", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-s", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--summarize", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--time", nargs="?", default=argparse.SUPPRESS)
  parser.add_argument("--time-style", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--help", action="store_true", default=argparse.SUPPRESS)
  base.check_args(args, parser)

  if uxy_args.long:
    fmtargs = ['--time', '--time-style=full-iso']
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = base.Format("USAGE    TIME                                FILE")
  else:
    fmtargs = []
    regexp = re.compile(r'\s*([^\s]*)\s+(.*)')
    fmt = base.Format("USAGE    FILE")

  proc = base.launch(['du'] + fmtargs + args[1:])
  base.writeout(fmt.render())
  for ln in proc:
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    if uxy_args.long:
      time = "%sT%s%s:%s" % (m.group(2), m.group(3), m.group(4)[:-2],
        m.group(4)[-2:])
      fields.append(base.encode_field(m.group(1)))
      fields.append(base.encode_field(time))
      fields.append(base.encode_field(m.group(5)))
    else:
      for i in range(1, regexp.groups + 1):
        fields.append(base.encode_field(m.group(i)))
    base.writeout(fmt.render(fields))


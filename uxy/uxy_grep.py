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

from uxy import base

def grep(args, uxy_args):
  parser = argparse.ArgumentParser()
  subp = parser.add_subparsers().add_parser('grep', help="find regexp in UXY")
  subp.add_argument('conditions', nargs="*", metavar="CONDITION",
    help="list of regexp and field pairs; regexp without a field matches any field")
  args = parser.parse_args(args)

  # Use the old headers.
  s = base.stdin.readline()
  fmt = base.Format(s)
  base.writeline(fmt.render())

  # Precompile the conditions.
  conds = []
  for i in range(0, len(args.conditions), 2):
    if i + 1 >= len(args.conditions):
      field = None
    else:
      if not args.conditions[i + 1] in fmt.fields:
        continue
      field = fmt.fields.index(args.conditions[i + 1])
    conds.append((re.compile(args.conditions[i]), field))

  # Process the data.
  for ln in base.stdin:
    fields = base.split_fields(ln)
    match = True
    for c in conds:
      if c[1] == None:
        match2 = False
        for f in fields:
          m = c[0].search(f)
          if m:
            match2 = True
            break
        if not match2:
          match = False
          break
      else:
        m = c[0].search(fields[c[1]])
        if not m:
          match = False
          break
    if match:
      base.writeline(fmt.render(fields))
  return 0

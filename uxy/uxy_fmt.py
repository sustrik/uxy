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

from uxy import base

def fmt(args, uxy_args):
  parser = argparse.ArgumentParser()
  subp = parser.add_subparsers().add_parser('fmt',
    help="reformat UXY data")
  subp.add_argument('header', help="new UXY header")
  args = parser.parse_args(args)

  # Use the supplied format.
  fmt = base.Format(args.header)
  newhdr = base.split_fields(args.header)
  base.writeline(fmt.render())
  # Read the old format.
  s = base.stdin.readline()
  oldhdr = base.split_fields(s)
  # Process the data.
  for ln in base.stdin:
    oldfields = base.split_fields(ln)
    newfields = ['""'] * len(newhdr)
    for i in range(0, len(oldfields)):
      if i >= len(oldhdr):
        break
      oldname = oldhdr[i]
      if oldname not in newhdr:
        continue
      newfields[newhdr.index(oldname)] = oldfields[i]
    base.writeline(fmt.render(newfields))
  return 0

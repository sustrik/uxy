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

import io
import csv

from helpers import *

def from_csv(parser, args, uxy_args):
  subp = parser.add_subparsers().add_parser('from-csv',
    help="convert CSV to UXY")
  args = parser.parse_args(args)

  # Read the headers
  ln = trim_newline(sys.stdin.readline())
  r = csv.reader(io.StringIO(ln))
  for fields in r:
    fields = " ".join([encode_field(f) for f in fields])
    fmt = Format(fields)
    writeout(fields + "\n")
  for ln in sys.stdin:
    r = csv.reader(io.StringIO(trim_newline(ln)))
    for fields in r:
      fields = [encode_field(f) for f in fields]
      writeout(fmt.render(fields))

def to_csv(parser, args, uxy_args):
  subp = parser.add_subparsers().add_parser('to-csv',
    help="convert UXY to CSV")
  args = parser.parse_args(args)

  for ln in sys.stdin:
    fields = split_fields(trim_newline(ln))
    fields = [decode_field(f) for f in fields]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(fields)
    writeout(buf.getvalue())


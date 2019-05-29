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

import re

from helpers import *

def do_import(parser, args, uxy_args):
  subp = parser.add_subparsers().add_parser('import',
    help="convert arbitrary input to UXY")
  subp.add_argument('header', help="UXY header")
  subp.add_argument('regexp', help="regexp to parse the input lines")
  args = parser.parse_args(args)

  # Use the supplied format.
  fmt = Format(args.header)
  writeout(fmt.render())
  # Parse the data.
  regexp = re.compile(args.regexp)
  for ln in sys.stdin:
    m = regexp.match(trim_newline(ln))
    # Non-matching lines are ignored.
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups + 1):
      fields.append(encode_field(m.group(i)))
    writeout(fmt.render(fields))

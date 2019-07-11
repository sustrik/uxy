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

def trim(args, uxy_args):
  parser = argparse.ArgumentParser()
  subp = parser.add_subparsers().add_parser('trim',
    help="trim long fields to fit into columns")
  args = parser.parse_args(args)

  # Read the headers.
  s = base.stdin.readline()
  fmt = base.Format(s)
  # Adjust the column widths so that at least quoted elipsis fits in.
  for i in range(0, len(fmt.widths) - 1):
    fmt.widths[i] = max(fmt.widths[i], 6)
  base.writeline(fmt.render())
  # Process the records.
  for ln in base.stdin:
    fields = base.split_fields(ln)
    # Get rid of unnamed fields.
    fields = fields[:len(fmt.widths)]
    # Trim the long fields. Last field is never trimmed.
    for i in range(0, len(fields) - 1):
      if len(fields[i]) > fmt.widths[i] - 1:
        if fields[i].startswith('"') and fields[i].endswith('"'):
            fields[i] = '"' + fields[i][1:fmt.widths[i] - 6] + '..."'
            if fields[i] == '"..."':
              fields[i] = '...'
        else:
            fields[i] = fields[i][:fmt.widths[i] - 4] + "..."
    base.writeline(fmt.render(fields))
  return 0

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

import json

from tools import base

def from_json(parser, args, uxy_args):
  subp = parser.add_subparsers().add_parser('from-json',
    help="convert JSON to UXY")
  args = parser.parse_args(args)

  # Read the entire input.
  s = ""
  for ln in base.stdin:
    s += ln
  root = json.loads(s)
  # Normalize the JSON. Collect the field names along the way.
  fields = {}
  if not isinstance(root, list):
    root = [root]
  for i in range(0, len(root)):
    if not isinstance(root[i], dict):
      root[i] = {"COL1": root[i]}
    for k, _ in root[i].items():
      fields[k] = None
  # Fields will go to the output in alphabetical order.
  fields = sorted(fields)
  # Collect the data. At the same time adjust the format sa that data fit in.
  fmt = base.Format(" ".join([base.encode_field(f) for f in fields]))
  records = []
  for i in range(0, len(root)):
    record = []
    for f in fields:
      if f in root[i]:
        record.append(base.encode_field(str(root[i][f])))
      else:
        record.append('""')
    fmt.adjust(record)
    records.append(record)
  # Write the result to output.
  base.writeline(fmt.render())
  for r in records:
    base.writeline(fmt.render(r))
  return 0

def to_json(parser, args, uxy_args):
  subp = parser.add_subparsers().add_parser('to-json',
    help="convert UXY to JSON")
  args = parser.parse_args(args)

  s = base.stdin.readline()
  hdr = base.split_fields(s)
  base.writeline("[\n")
  first = True
  for ln in base.stdin:
    if not first:
      base.writeline(",\n")
    else:
      first = False
    fields = base.split_fields(ln)
    item = {}
    for i in range(0, len(fields)):
      item[base.decode_field(hdr[i])] = base.decode_field(fields[i])
    base.writeline(json.dumps(item, indent=4))
  base.writeline("\n]\n")
  return 0

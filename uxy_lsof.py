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
import itertools
import re

import base

def lsof(parser, args, uxy_args):
  proc = base.launch(['lsof', '+c', '0'] + args[1:])
  hdr = proc.readline()
  parts = re.split("(\s+)", hdr)
  pos = [len(p) for p in list(itertools.accumulate(parts))]
  r1 = re.compile(r'([^\s]*)\s+([^\s]*)')
  fmt = base.Format("COMMAND             PID    TID    USER           FD      TYPE    DEVICE             SIZEOFF   NODE       NAME")
  base.writeline(fmt.render())
  for ln in proc:
    fields = []
    m = r1.match(ln[:pos[2]])
    if not m:
      continue
    fields.append(m.group(1))
    fields.append(m.group(2))
    fields.append(ln[pos[2]:pos[4]].strip())
    fields.append(ln[pos[4]:pos[6]].strip())
    fields.append(ln[pos[6]:pos[8] + 1].strip())
    fields.append(ln[pos[8] + 1:pos[10]].strip())
    fields.append(ln[pos[10]:pos[12]].strip())
    fields.append(ln[pos[12]:pos[14]].strip())
    fields.append(ln[pos[14]:pos[16]].strip())
    fields.append(ln[pos[16]:].strip())
    fields = [base.encode_field(f) for f in fields]
    base.writeline(fmt.render(fields))

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
import itertools
import subprocess

from helpers import *

def netstat(parser, args, uxy_args):
  proc = subprocess.Popen(['netstat', '--inet'] + args[1:], stdout=subprocess.PIPE)
  # Skip header line.
  proc.stdout.readline()
  hdr = trim_newline(proc.stdout.readline().decode("utf-8"))
  parts = re.split("(\s+)", hdr)
  pos = [len(p) for p in list(itertools.accumulate(parts))]
  fmt = Format("PROTO  RECVQ  SENDQ  LOCAL            REMOTE                      STATE")
  writeout(fmt.render())
  for ln in proc.stdout:
    ln = trim_newline(ln.decode("utf-8"))
    fields = []
    fields.append(ln[0:pos[0]].strip())
    fields.append(ln[pos[0]:pos[2]].strip())
    fields.append(ln[pos[2]:pos[4]].strip())
    fields.append(ln[pos[4]:pos[8]].strip())
    fields.append(ln[pos[8]:pos[13]].strip())
    fields.append(ln[pos[13]:].strip())
    fields = [encode_field(f) for f in fields]
    writeout(fmt.render(fields))


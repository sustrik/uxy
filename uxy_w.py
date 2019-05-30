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
import subprocess

import helpers

def w(parser, args, uxy_args):
  parser = argparse.ArgumentParser("uxy w", add_help=False)
  parser.add_argument("-h", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--no-header", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-s", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--short", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-f", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--from", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-o", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--old-style", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--help", action="store_true", default=argparse.SUPPRESS)
  helpers.check_args(args, parser)

  proc = subprocess.Popen(['w', '--no-header'] + args[1:], stdout=subprocess.PIPE)
  regexp = re.compile(r'([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
  fmt = helpers.Format("USER     TTY    FROM    LOGIN    IDLE    JCPU    PCPU    WHAT")
  helpers.writeout(fmt.render())
  for ln in proc.stdout:
    ln = helpers.trim_newline(ln.decode("utf-8"))
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups + 1):
      fields.append(helpers.encode_field(m.group(i)))
    helpers.writeout(fmt.render(fields))


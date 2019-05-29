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

from helpers import *

def ls(parser, args, uxy_args):
  parser = argparse.ArgumentParser("uxy ls", add_help=False)
  parser.add_argument("--author", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-b", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--escape", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-C", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--color", nargs="?", default=argparse.SUPPRESS)
  parser.add_argument("-D", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-f", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--format", nargs="?", default=argparse.SUPPRESS)
  parser.add_argument("--full-time", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-g", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-h", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--human-readable", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--si", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-G", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--no-group", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-i", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--inode", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-k", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--kibibytes", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-l", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-m", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-N", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--literal", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-o", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-q", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--hide-control-chars", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-Q", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--quote-name", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--quoting-style", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-s", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--time", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--time-style", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-T", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--tabsize", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-w", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("--width", nargs=1, default=argparse.SUPPRESS)
  parser.add_argument("-x", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-Z", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--context", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("-1", action="store_true", default=argparse.SUPPRESS)
  parser.add_argument("--help", action="store_true", default=argparse.SUPPRESS)
  check_args(args, parser)

  if uxy_args.long:
    fmtargs = ['-lNisZw0', '--time-style=full-iso']
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+(.)([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = Format("INODE   BLOCKS TYPE PERMISSIONS LINKS OWNER      GROUP      CONTEXT SIZE         TIME                                  NAME")
  else:
    fmtargs = ['-lNw0', '--time-style=full-iso']
    regexp = re.compile(r'\s*(.)([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = Format("TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME")

  proc = subprocess.Popen(['ls'] + fmtargs + args[1:], stdout=subprocess.PIPE)
  writeout(fmt.render())
  path = ""
  for ln in proc.stdout:
    ln = trim_newline(ln.decode("utf-8"))
    if ln.startswith('total'):
      continue
    if ln == "":
      # When running with -R this is the name of the directory.
      ln = trim_newline(proc.stdout.readline().decode("utf-8"))
      if ln.endswith(":"):
        path = ln[:-1] + "/"
      continue
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups - 3):
      fields.append(encode_field(m.group(i)))
    # Convert to actual ISO8601 format.
    time = "%sT%s%s:%s" % (
      m.group(regexp.groups - 3),
      m.group(regexp.groups - 2),
      m.group(regexp.groups - 1)[:-2],
      m.group(regexp.groups - 1)[-2:])
    fields.append(encode_field(time))
    fields.append(encode_field(path + m.group(regexp.groups)))
    writeout(fmt.render(fields))


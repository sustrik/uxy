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
import sys

from uxy import base

def _linux(args, uxy_args):
  parser = argparse.ArgumentParser("__main__.py top")
  parser.parse_args(args[1:])

  proc = base.launch(uxy_args, ['top', '-bn1'] + args[1:])
  # Skip the summary.
  for i in range(0, 7):
    proc.readline()

  if uxy_args.long:
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = base.Format("PID    USER     PR   NI   VIRT     RES      SHR      S  CPU   MEM   TIME        CMD")
  else:
    regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+[^\s]*\s+[^\s]*\s+[^\s]*\s+[^\s]*\s+[^\s]*\s+[^\s]*\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+(.*)')
    fmt = base.Format("PID    USER     CPU   MEM   TIME        CMD")

  base.writeline(fmt.render())
  for ln in proc:
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups + 1):
      fields.append(base.encode_field(m.group(i)))
    base.writeline(fmt.render(fields))
  return proc.wait()

def _bsd(args, uxy_args):
  parser = argparse.ArgumentParser("__main__.py top")
  parser.parse_args(args[1:])

  proc = base.launch(uxy_args, ['top', '-l 1'] + args[1:])
  # Skip the summary.
  for i in range(0, 12):
    proc.readline()

  regexp = re.compile(r'\s*([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+([^\s]*)\s+.*')
  fmt = base.Format("PID  CMD  CPU  TIME TH WQ PORTS MEM PURG CMPRS PGRP PPID STATE BOOSTS CPU_ME CPU_OTHRS UID FAULTS COW MSGSENT MSGRECV SYSBSD SYSMACH CSW PAGEINS IDLEW POWER INSTRS CYCLES USER")

  base.writeline(fmt.render())
  for ln in proc:
    m = regexp.match(ln)
    if not m:
      continue
    fields = []
    for i in range(1, regexp.groups + 1):
      fields.append(base.encode_field(m.group(i)))
    base.writeline(fmt.render(fields))
  return proc.wait()

def top(args, uxy_args):
  if uxy_args.platform.startswith("linux"):
    return _linux(args, uxy_args)
  else:
    return _bsd(args, uxy_args)

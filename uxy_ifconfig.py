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

def write_ifconfig_record(fmt, iface):
  fields = []
  for f in fmt.fields:
    if f in iface:
      fields.append(encode_field(iface[f]))
    else:
      fields.append(encode_field(""))
  writeout(fmt.render(fields))


def ifconfig(parser, args, uxy_args):
  parser = argparse.ArgumentParser("uxy ifconfig")
  parser.add_argument("-a", action="store_true", default=False,
    help=" display all interfaces which are currently available, even if down")
  parser.add_argument('interface', nargs="?", default=None,
    help="network interface to display")
  parser.parse_args(args[1:])

  if uxy_args.long:
    fmt = Format("NAME       INET-ADDR       INET-NETMASK       INET6-ADDR               INET6-PREFIXLEN INET6-SCOPEID ETHER-ADDR        MTU   INTERRUPT MEMORY              RX-PACKETS RX-BYTES     RX-ERRORS RX-DROPPED RX-OVERRUNS RX-FRAME TX-PACKETS TX-BYTES     TX-ERRORS TX-DROPPED TX-OVERRUNS TX-CARRIER TX-COLLISIONS TX-QUEUELEN FLAGS")
  else:
    fmt = Format("NAME       RX-PACKETS RX-BYTES     RX-ERRORS RX-DROPPED TX-PACKETS TX-BYTES     TX-ERRORS TX-DROPPED FLAGS")

  proc = subprocess.Popen(['ifconfig'] + args[1:], stdout=subprocess.PIPE)
  writeout(fmt.render())
  leading = re.compile("([^:]+):\s+flags=\d+<([^>]*)>\s+mtu\s+(\d+)")
  first = True
  iface = {}
  for ln in proc.stdout:
    ln = trim_newline(ln.decode("utf-8"))
    if len(ln) == 0:
      continue
    if ln[0] != ' ':
      if not first:
        # push the current record
        write_ifconfig_record(fmt, iface)
        iface = {}
      else:
        first = False
      # Parse the leading line.
      m = leading.match(ln)
      if not m:
        sys.exit(1)
      iface["NAME"] = m.group(1)
      iface["FLAGS"] = m.group(2)
      iface["MTU"] = m.group(3)
    else:
      # Parse the trailing line.
      parts = ln.split()
      if parts[0] == "ether":
        iface["ETHER-ADDR"] = parts[1]
        iface["TX-QUEUELEN"] = parts[3]
      elif parts[0] == "inet":
        iface["INET-ADDR"] = parts[1]
        iface["INET-NETMASK"] = parts[3]
      elif parts[0] == "inet6":
        iface["INET6-ADDR"] = parts[1]
        iface["INET6-PREFIXLEN"] = parts[3]
        iface["INET6-SCOPEID"] = parts[5]
      elif parts[0] == "loop":
        iface["TX-QUEUELEN"] = parts[2]
      elif parts[0] == "device":
        iface["INTERRUPT"] = parts[2]
        iface["MEMORY"] = parts[4]
      elif parts[0] == "TX":
        if parts[1] == "packets":
          iface["TX-PACKETS"] = parts[2]
          iface["TX-BYTES"] = parts[4]
        else:
          iface["TX-ERRORS"] = parts[2]
          iface["TX-DROPPED"] = parts[4]
          iface["TX-OVERRRUNS"] = parts[6]
          iface["TX-CARRIER"] = parts[8]
          iface["TX-COLLISIONS"] = parts[10]
      elif parts[0] == "RX":
        if parts[1] == "packets":
          iface["RX-PACKETS"] = parts[2]
          iface["RX-BYTES"] = parts[4]
        else:
          iface["RX-ERRORS"] = parts[2]
          iface["RX-DROPPED"] = parts[4]
          iface["RX-OVERRRUNS"] = parts[6]
          iface["RX-FRAME"] = parts[8]
  if not first:
    write_ifconfig_record(fmt, iface)


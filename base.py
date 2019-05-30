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

import sys
import unicodedata
import subprocess

def trim_newline(s):
  if s.endswith('\n'):
    return s[:-1]
  return s

def writeline(s):
 try:
   sys.stdout.write(s)
 except BrokenPipeError:
   # The next command in the pipeline is not interested in more data.
   # We can shut down cleanly.
   sys.exit(0)

ESCAPE_SEQUENCES1 = {
  't':  '\t',
  'n':  '\n',
  '"':  '"',
  '\\': '\\',
}


ESCAPE_SEQUENCES2 = {
  '\t':  't',
  '\n':  'n',
  '"':  '"',
  '\\': '\\',
}


# Convert uxy field into a string.
def decode_field(s):
  # Replace control characters by question marks.
  s = "".join((c if unicodedata.category(c)[0] != "C" else '?') for c in s)
  if not (s.startswith('"') and s.endswith('"')):
    return s
  # Quoted field.
  s = s[1:-1]
  # Expand escape sequences.
  f = ""
  j = 0
  while j < len(s):
    if s[j] == '\\':
      if j + 1 >= len(s):
        f += "?"
        j += 1;
        continue
      if s[j + 1] not in ESCAPE_SEQUENCES1:
        f += "?"
        j += 2
        continue
      f += ESCAPE_SEQUENCES1[s[j + 1]]
      j += 2
      continue
    f += s[j]
    j += 1
  return f


# Convert arbitrary string into a uxy field.
def encode_field(s):
  # Empty string converts to "".
  if s == "":
    return '""  '
  # Check whether the string contains any special characters.
  special = False
  if '"' in s or ' ' in s:
    special = True
  else:
    for c in s:
      if unicodedata.category(c)[0] == "C":
        special = True
        break
  if not special:
    return s
  # Quoted field is needed.
  f = '"'
  for c in s:
    if c in ESCAPE_SEQUENCES2:
      f += ESCAPE_SEQUENCES2[c]
      continue
    f += c
  return f + '"'

UNQUOTED = 1
QUOTED = 2
ESCAPE = 3
TRAILING = 4

# Given a line, this function splits it into individual uxy fields and
# field widths.
def split_fields_widths(s):
  fields = []
  widths = []
  state = TRAILING
  field = ""
  width = 0
  for c in s:
    if state == UNQUOTED:
      if c == ' ':
        width += 1
        state = TRAILING
      else:
        field += c
        width += 1
    elif state == QUOTED:
      if c == "\\":
        field += c
        width += 1
        state = ESCAPE
      elif c == '"':
        field += c
        width += 1
        state = TRAILING
      else:
        field += c
        width += 1      
    elif state == ESCAPE:
      field += c
      width += 1
      state = QUOTED
    elif state == TRAILING:
      if c == " ":
        width += 1
      else:
        if len(field) > 0:
          fields.append(field)
          widths.append(width)
        field = c
        width = 1
        if c == '"':
          state = QUOTED
        else:
          state = UNQUOTED
  if len(field) > 0:
    fields.append(field)
    widths.append(width)
  return (fields, widths)


# Given a line, this function splits it into individual uxy fields.
def split_fields(s):
  fields, _ = split_fields_widths(s)
  return fields


class Format:

  # Create a format from a list of fields.
  # The values of the fields will be used as column names.
  def __init__(self, fmt):
    self.fields, self.widths = split_fields_widths(fmt)

  # Adjust the format so that the fields fit in.
  def adjust(self, fields):
    for i in range(0, len(fields)):
       self.widths[i] = max(self.widths[i], len(fields[i]) + 1)

  # Renders the supplied fields according to the format.
  # If fields is None, it renders the header itself.
  def render(self, fields=None):
    if fields == None:
      fields = self.fields
    broken = False
    res = ""
    for i in range(0, len(fields)):
      if broken or len(fields[i]) + 1 > self.widths[i]:
        broken = True
        res += fields[i] + " "
      else:
        res += fields[i] + " " * (self.widths[i] - len(fields[i]))
    return res + "\n"


# Makes sure that arguments specified by the parser and not supplied
# by the user.
def check_args(args, parser):
  found, _ = parser.parse_known_args(args)
  offending = list(vars(found).keys())
  if len(offending) > 0:
    print(
      "uxy: argument '%s' is overriden by uxy, cannot be set by the user" %
        offending[0],
      file=sys.stderr)
    sys.exit(1)

# Make reading from the pipe much like reading from a file.
class PipeReader(object):
  def __init__(self, pipe):
    self.pipe = pipe

  def __iter__(self):
    return self

  def __next__(self):
    return self.readline()
 
  def readline(self):
    ln = self.pipe.readline()
    if not ln:
      raise StopIteration()
    return ln.decode("utf-8").rstrip("\n")

def launch(uxy_args, args):
  if uxy_args.test:
    return stdin
  proc = subprocess.Popen(args, stdout=subprocess.PIPE)
  return PipeReader(proc.stdout)

# Like sys.stdin but trims newlines from the end of the lines.
class StdinReader(object):
  def __init__(self):
    pass

  def __iter__(self):
    return self

  def __next__(self):
    return self.readline()
 
  def readline(self):
    ln = sys.stdin.readline()
    if not ln:
      raise StopIteration()
    return ln.rstrip("\n")

stdin = StdinReader()

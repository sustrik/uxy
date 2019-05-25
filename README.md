# UXY: Adding structure to the UNIX tools

Treating everything as a string is the way through which the great power and
versatility of UNIX tools is achieved. However, sometimes the constant
parsing of strings gets a bit cumbersome.

UXY is a tool to manipulate UXY format, which is a basically
a two-dimensional table that's both human- and machine-readable.

The format is deliberately designed to be as similar to the output of
standard tools, such as `ls` or `ps`, as possible.

UXY tool also wraps some common UNIX tools and exports their output in
UXY format. Along with converters from/to other common data formats
(e.g. JSON) it is meant to allow for quick and painless access to the data.

### Examples

<pre>
<b>$ uxy ls</b>
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME 
-    rw-r--r--   1     martin     martin     7451         "2019-05-19 23:35:13.552174105 +0200" README.md 
-    rwxr-xr-x   1     martin     martin     11518        "2019-05-20 04:08:36.847163604 +0200" uxy
</pre>

<pre>
<b>$ uxy ls | uxy reformat "NAME SIZE"</b>
NAME SIZE 
README.md 7451 
uxy  11518 
</pre>

<pre>
<b>$ uxy ls | uxy reformat "NAME SIZE" | uxy align</b>
NAME      SIZE
README.md 7451 
uxy       11518
</pre>

<pre>
<b>$ uxy top | uxy reformat "PID CPU COMMAND" | uxy to-json</b>
[
    {
        "PID": "4704",
        "CPU": "12.5",
        "COMMAND": "top"
    },
    {
        "PID": "2903",
        "CPU": "6.2",
        "COMMAND": "Web Content"
    },
    {
        "PID": "1",
        "CPU": "0.0",
        "COMMAND": "systemd"
    }
]
</pre>

<pre>
<b>$ uxy ls | uxy grep test NAME</b>
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME 
-    rw-r--r--   1     martin     martin     45           "2019-05-20 05:07:05.095066240 +0200" test.csv 
-    rw-r--r--   1     martin     martin     84           "2019-05-20 19:32:37.332820969 +0200" test.txt 
-    rw-r--r--   1     martin     martin     75           "2019-05-20 17:28:47.942511346 +0200" test.uxy
</pre>

<pre>
<b>$ uxy ps | uxy to-json | jq '.[].CMD'</b>
"bash"
"uxy"
"uxy"
"jq"
"ps"
</pre>

<pre>
<b>$ cat test.csv</b>
NAME,TIME
Quasimodo,14:30
Moby Dick,14:22
<b>$ cat test.csv | uxy from-csv | uxy align</b>
NAME        TIME
Quasimodo   14:30 
"Moby Dick" 14:22 
</pre>

# UXY format

### Rationale

UXY format is designed with the following requirements in mind:

- It should be human-readable.
- It should be as similar to the output of standard tools, such as `ls` or `ps`,
  as possible.
- At the same time it should be unambiguous and thus parsable in deterministic
  manner.
- It should be, to some minimal extent, self-describing (column names).
- It should work well with infinite streams (think, for example, the output of
  `tail` command).
- It should be resilient. No possible input should crash the tool.

### Records and fields

- UXY format is a possibly infinite list of lines separated by newlines.
- Each line is composed of fields separated by arbitrary number of spaces.
- Fields starting AND ending with a double quote are treated in a special way:
  - The delimiting double-quote characters themselves are ignored.
  - The characters inside the quotes, including spaces, are taken as they are.
  - The only exception are the characters preceded by backslash. These are
    encoded as follows:
    - `\"` double quote
    - `\\` backslash
    - `\t` tab
    - `\n` newline
    - any other escape sequence MUST be interpreted as `?` (question mark)
      character.
- Any control characters (e.g. `TAB`) MUST be interpreted as `?` (question mark)
  characters.

### Header

- First line of UXY format is the header.
- The format of the header line is identical to any other UXY line,
  however, its semantics differ.
- The value of a field in the header is the name of that particular column.
- The spacing of the fields in the header is a hint for the tools. They SHOULD
  try to align the data with the headers.

### Interactions between headers and records

- Fields may or may not be aligned with each other or with the headers.
- If there are less fields in a record than in the header the missing values
  are assumed to be empty strings.
- It is valid to for a record to have more fields than the header.
  The tools should consider the name of such column to be an empty string.

### Example

<pre>
NAME  AGE ADDRESS
Alice 25  "Main Road 1, London" "Let's use this unnamed field for comments."
Bob   23  ""
Carol 55  "Hotel \"Excelsior\", New York"
  Dylan             15
</pre>

# TOOLS

All UXY tools take input from stdin and write the result to stdout.

The tools follow the Postel's principle: "Be liberal in what you accept,
conservative in what you output." They accept any UXY input, but
they try to align the fields in the output to make it more convenient to read.

- **[uxy align](doc/align.md)**
- **[uxy du](doc/du.md)**
- **[uxy from-csv](doc/from-csv.md)**
- **[uxy from-json](doc/from-json.md)**
- **[uxy from-yaml](doc/from-yaml.md)**
- **[uxy grep](doc/grep.md)**
- **[uxy import](doc/import.md)**
- **[uxy ls](doc/ls.md)**
- **[uxy lsof](doc/lsof.md)**
- **[uxy netstat](doc/netstat.md)**
- **[uxy ps](doc/ps.md)**
- **[uxy reformat](doc/reformat.md)**
- **[uxy to-csv](doc/to-csv.md)**
- **[uxy to-json](doc/to-json.md)**
- **[uxy to-yaml](doc/to-yaml.md)**
- **[uxy top](doc/top.md)**
- **[uxy trim](doc/trim.md)**
- **[uxy w](doc/w.md)**


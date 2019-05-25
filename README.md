# UXY: Adding structure to the UNIX tools

Treating everything as a string is the way through which the great power and
versatility of UNIX tools is achieved. However, sometimes the constant
parsing of strings gets a bit cumbersome.

UXY is a tool to manipulate [UXY format](doc/uxy-format.md), which is
basically a two-dimensional table that's both human- and machine-readable.

The format is deliberately designed to be as similar to the output of
standard tools, such as `ls` or `ps`, as possible.

UXY tool also wraps some common UNIX tools and exports their output in
UXY format. Along with converters from/to other common data formats
(e.g. JSON) it is meant to allow for quick and painless access to the data.

### Examples

<pre>
<b>$ uxy ls</b>
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE    TIME                                  NAME 
-    rw-r--r--   1     martin     martin     7451    "2019-05-19 23:35:13.552174105 +0200" README.md 
-    rwxr-xr-x   1     martin     martin     11518   "2019-05-20 04:08:36.847163604 +0200" uxy
</pre>

<pre>
<b>$ uxy ls | uxy fmt "NAME SIZE"</b>
NAME SIZE 
README.md 7451 
uxy  11518 
</pre>

<pre>
<b>$ uxy ls | uxy fmt "NAME SIZE" | uxy align</b>
NAME      SIZE
README.md 7451 
uxy       11518
</pre>

<pre>
<b>$ uxy top | uxy fmt "PID CPU COMMAND" | uxy to-json</b>
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
- **[uxy fmt](doc/fmt.md)**
- **[uxy to-csv](doc/to-csv.md)**
- **[uxy to-json](doc/to-json.md)**
- **[uxy to-yaml](doc/to-yaml.md)**
- **[uxy top](doc/top.md)**
- **[uxy trim](doc/trim.md)**
- **[uxy w](doc/w.md)**


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
-    rw-r--r--   1     martin     martin     3204    2019-05-25T15:44:46.371308721+02:00   README.md
-    rwxr-xr-x   1     martin     martin     25535   2019-05-25T16:29:28.518397541+02:00   uxy
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
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE    TIME                                  NAME 
-    rw-r--r--   1     martin     martin     45      2019-05-25T16:09:58.755551983+02:00   test.csv 
-    rw-r--r--   1     martin     martin     84      2019-05-25T16:09:58.755552856+02:00   test.txt 
-    rw-r--r--   1     martin     martin     75      2019-05-25T16:09:58.755559998+02:00   test.uxy
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

### UXY tools

All UXY tools take input from stdin and write the result to stdout.

The tools follow the Postel's principle: "Be liberal in what you accept,
conservative in what you output." They accept any UXY input, but
they try to align the fields in the output to make it more convenient to read.

- **[uxy align](doc/align.md)**
- **[uxy from-csv](doc/from-csv.md)**
- **[uxy from-json](doc/from-json.md)**
- **[uxy from-yaml](doc/from-yaml.md)**
- **[uxy grep](doc/grep.md)**
- **[uxy import](doc/import.md)**
- **[uxy fmt](doc/fmt.md)**
- **[uxy to-csv](doc/to-csv.md)**
- **[uxy to-json](doc/to-json.md)**
- **[uxy to-yaml](doc/to-yaml.md)**
- **[uxy trim](doc/trim.md)**

### Wrapped UNIX tools

Any argument that could be passed to the original tool can also be passed to
the UXY-wrapped version of the tool.

The exception are the arguments that modify how the output looks like. UXY
manages those arguments itself. The only control you have over the output is
to either print the default (short) set of result fields (mostly defined
as "the most useful info that fits on page") or long set of result fields
("all the information UXY was able to extract"):

<pre>
<b>$ uxy -l ps</b>
</pre>

When running with `-l` option it often happens that the output exceeds the
terminal width, gets wrapped and unreadable. In such cases you can either
filter out just the fields you are intersed in using `fmt` subcommand or
convert the result to YAML which happens to rendev each field on a separate
line:

<pre>
<b>$ uxy -l ifconfig | uxy fmt "NAME         INET-ADDR"</b>
NAME         INET-ADDR 
enp0s31f6    ""       
lo           127.0.0.1 
wlp3s0       192.168.1.7
<b>$ uxy -l ifconfig | uxy to-yaml</b>
- ETHER-ADDR: e4:42:a6:f4:1d:02
  FLAGS: UP,BROADCAST,RUNNING,MULTICAST
  INET-ADDR: 192.168.1.7
  INET-NETMASK: 255.255.255.0
  INET6-ADDR: fe80::fd53:a17f:12ce:38a8
  INET6-PREFIXLEN: '64'
  INET6-SCOPEID: 0x20<link>
  ...
</pre> 

- **[uxy du](doc/du.md)**
- **[uxy ifconfig](doc/ifconfig.md)**
- **[uxy ls](doc/ls.md)**
- **[uxy lsof](doc/lsof.md)**
- **[uxy netstat](doc/netstat.md)**
- **[uxy ps](doc/ps.md)**
- **[uxy top](doc/top.md)**
- **[uxy w](doc/w.md)**


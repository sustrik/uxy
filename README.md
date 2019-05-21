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

```
$ uxy ls
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME 
-    rw-r--r--   1     martin     martin     7451         "2019-05-19 23:35:13.552174105 +0200" README.md 
-    rwxr-xr-x   1     martin     martin     11518        "2019-05-20 04:08:36.847163604 +0200" uxy
```

```
$ uxy ls | uxy reformat "NAME SIZE"
NAME SIZE 
README.md 7451 
uxy  11518 
```

```
$ uxy ls | uxy reformat "NAME SIZE" | uxy align
NAME      SIZE
README.md 7451 
uxy       11518
```

```
$ uxy top | uxy reformat "PID CPU COMMAND" | uxy to-json
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
```

```
$ uxy ps | uxy to-json | jq '.[].CMD'
"bash"
"uxy"
"uxy"
"jq"
"ps"
```

```
$ cat test.csv 
NAME,TIME
Quasimodo,14:30
Moby Dick,14:22
$ cat test.csv | uxy from-csv | uxy align
NAME        TIME
Quasimodo   14:30 
"Moby Dick" 14:22 
```

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

```
NAME  AGE ADDRESS
Alice 25  "Main Road 1, London" "Let's use this unnamed field for comments."
Bob   23  ""
Carol 55  "Hotel \"Excelsior\", New York"
  Dylan             15
```

# TOOLS

All UXY tools take input from stdin and write the result to stdout.

The tools follow the Postel's principle: "Be liberal in what you accept,
conservative in what you output." They accept any UXY input, but
they try to align the fields in the output to make it more convenient to read.

- **[uxy align](#uxy-align)**
- **[uxy du](#uxy-du)**
- **[uxy from-csv](#uxy-from-csv)**
- **[uxy from-json](#uxy-from-json)**
- **[uxy from-yaml](#uxy-from-yaml)**
- **[uxy ls](#uxy-ls)**
- **[uxy lsof](#uxy-lsof)**
- **[uxy ps](#uxy-ps)**
- **[uxy re](#uxy-re)**
- **[uxy reformat](#uxy-reformat)**
- **[uxy to-csv](#uxy-to-csv)**
- **[uxy to-json](#uxy-to-json)**
- **[uxy to-yaml](#uxy-to-yaml)**
- **[uxy top](#uxy-top)**
- **[uxy trim](#uxy-trim)**
- **[uxy w](#uxy-w)**

### uxy align

Aligns the data with the headers. This is done by resizing the columns so that
even the longest value fits into the column.

```
$ ls -l | uxy re "TIME NAME" ".* +(.*) +(.*)" | uxy align
TIME  NAME
14:36 README.md 
14:22 uxy
```

This command doesn't work with infinite streams.

### uxy du

Wraps `du` tool and outputs the results in UXY format.

```
$ uxy du
USAGE    FILE
12       ./.git/objects/56 
12       ./.git/objects/62 
12       ./.git/objects/9d 
8        ./.git/objects/04 
8        ./.git/objects/43 
932      ./.git/objects 
1096     ./.git 
48       ./test 
1192     . 
```

### uxy from-csv

Converts from CSV to UXY format.

```
$ cat test.csv 
NAME,TIME
Quasimodo,14:30
Moby Dick,14:22
$ cat test.csv | uxy from-csv | uxy align
NAME        TIME
Quasimodo   14:30 
"Moby Dick" 14:22 
```

### uxy from-json

Converts from JSON to UXY format.

```
$ cat test.json 
[
    {"Name": "Quasimodo", "Time": "14:30"},
    {"Name": "Moby Dick", "Time": "14:22"}
]
$ uxy from-json < test.json 
Name        Time
Quasimodo   14:30 
"Moby Dick" 14:22
```

### uxy from-yaml

Converts from YAML to UXY format.

```
$ cat test.yml 
- Name: Mercury
  Diameter: 4880 km
- Name: Venus
  Diameter: 12103 km
- Name: Earth
  Diameter: 12742 km
  Color: Blue
$ uxy from-yaml < test.yml 
Color Diameter   Name
""    "4880 km"  Mercury 
""    "12103 km" Venus
Blue  "12742 km" Earth
```

### uxy ls

Wraps `ls` tool and outputs the results in UXY format.

```
$ uxy ls
TYPE PERMISSIONS LINKS OWNER      GROUP      SIZE         TIME                                  NAME 
-    rw-r--r--   1     martin     martin     7451         "2019-05-19 23:35:13.552174105 +0200" README.md 
-    rwxr-xr-x   1     martin     martin     11518        "2019-05-20 04:08:36.847163604 +0200" uxy 
```

### uxy lsof

Wraps `lsof` tool and outputs the results in UXY format.

```
$ uxy lsof
COMMAND             PID    TID    USER           FD      TYPE    DEVICE             SIZEOFF   NODE       NAME
AudioIPC1           28097  28858  martin         mem     REG     259,2              5288      2236410    /var/cache/fontconfig/6afa.cache-7 
AudioIPC1           28097  28858  martin         mem     REG     259,2              2552      2228534    /var/cache/fontconfig/e0aa.cache-7 
AudioIPC1           28097  28858  martin         0r      CHR     1,3                0t0       6          /dev/null 
AudioIPC1           28097  28858  martin         1u      unix    0x0000000000000000 0t0       32328      type=STREAM 
AudioIPC1           28097  28858  martin         2u      unix    0x0000000000000000 0t0       32329      type=STREAM 
AudioIPC1           28097  28858  martin         3u      unix    0x0000000000000000 0t0       2115911    type=STREAM 
AudioIPC1           28097  28858  martin         4u      unix    0x0000000000000000 0t0       2062380    type=SEQPACKET 
AudioIPC1           28097  28858  martin         5u      unix    0x0000000000000000 0t0       2062383    type=SEQPACKET 
AudioIPC1           28097  28858  martin         6r      REG     0,24               276       3          "/dev/shm/org.chromium.SK1kmw (deleted)" 
AudioIPC1           28097  28858  martin         7w      FIFO    0,12               0t0       2115912    pipe 
AudioIPC1           28097  28858  martin         8r      FIFO    0,12               0t0       2113268    pipe 
AudioIPC1           28097  28858  martin         9u      sock    0,9                0t0       2116129    "protocol: UNIX" 
```

### uxy ps

Wraps `ps` tool and outputs the results in UXY format.

```
$ uxy ps
PID      TTY      TIME       CMD 
20829    pts/1    00:00:00   bash 
29944    pts/1    00:00:00   uxy 
29945    pts/1    00:00:00   ps
```

### uxy re

Reads the lines of the input and parses each one using the supplied regular
expression. Matched groups are then assigned to the fields specified in
the header.

```
$ ls -l | uxy re "TIME NAME" ".* +(.*) +(.*)"
TIME NAME 
14:28 README.md
14:22 uxy
```

### uxy reformat

Takes an UXY input and reformats it according to the supplied headers.

It allows for:

- reordering of columns
- resizing of columns
- dropping columns
- adding new columns

```
$ cat test.uxy 
TIME  NAME
15:03 README.md 
16:08 uxy
$ uxy reformat "NAME          TIME" < test.uxy 
NAME          TIME 
README.md     15:03 
uxy           16:08 
```

### uxy to-csv

Converts UXY format to CSV.

```
$ uxy ls | uxy to-csv
TYPE,PERMISSIONS,LINKS,OWNER,GROUP,SIZE,TIME,NAME
-,rw-r--r--,1,martin,martin,7419,2019-05-20 04:28:47.211667681 +0200,README.md
-,rwxr-xr-x,1,martin,martin,11912,2019-05-20 04:41:35.316650681 +0200,uxy
```

### uxy to-json

Converts UXY format to JSON.

```
$ ls -l | uxy re "time name" ".* +(.*) +(.*)" | uxy to-json
[
    {
        "time": "14:22",
        "name": "README.md"
    },
    {
        "time": "14:22",
        "name": "uxy"
    }
]
```

### uxy to-yaml

Converts UXY format to YAML.

```
$ uxy ps | uxy to-yaml
- PID: '512'
  TIME: 00:00:00 uxy
  TTY: pts/22
- PID: '513'
  TIME: 00:00:00 uxy
  TTY: pts/22
- PID: '514'
  TIME: 00:00:00 ps
  TTY: pts/22
- CMD: bash
  PID: '12392'
  TIME: 00:00:01
  TTY: pts/22
```

### uxy top

Runs `top` tool in one-off manner and outputs the results in UXY format.

```
$ ./uxy top
PID    USER     PR   NI   VIRT     RES      SHR      S CPU   MEM   TIME       COMMAND 
4529   martin   20   0    41924    3708     3144     R 18.8  0.0   0:00.03    top
1      root     20   0    225916   9640     6600     S 0.0   0.1   1:57.75    systemd 
2      root     20   0    0        0        0        S 0.0   0.0   0:00.52    kthreadd 
4      root     0    -20  0        0        0        I 0.0   0.0   0:00.00    kworker/0:0H 
6      root     0    -20  0        0        0        I 0.0   0.0   0:00.00    mm_percpu_wq
```

### uxy trim

Trims any fields that exceed the width of the column as specified in the
header. The new value will end with three dots (`...`) to give a visual hint
that the field was trimmed.

The last column is treated as if it had infinite width and thus the values
in the last column are never truncated.

Unnamed fields are dropped.

```
$ cat test.uxy 
NAME     SIZE 
README.md 8060 
test.csv 45
test     0
uxy      13458 
$ cat test.uxy | uxy trim
NAME     SIZE 
READM... 8060 
test.csv 45
test     0
uxy      13458 
```

### uxy w

Wraps `w` tool and outputs the results in UXY format.

```
USER     TTY    FROM    LOGIN    IDLE    JCPU    PCPU    WHAT 
martin   :0     :0      03May19  ?xdm?   1:08m   0.03s   "/usr/bin/foo --bar"
```

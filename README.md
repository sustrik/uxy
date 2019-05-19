# UXY adds structure to the standard UNIX tools

Treating everything as a string is the way through which the great power and
verstatility of UNIX tools is achieved. However, sometimes the constant
parsing of strings gets a bit cumbersome.

UXY is a tool to manipulate the UXY format, which is a basically
a two-dimenstional table that's both human- and machine-readable.

# UXY format

## Records and fields

- UXY format is a possibly infinite list of lines separated by newlines.
  Each line is a data record.
- Each line is composed of fields separated by arbitrary number spaces.
- Fields starting AND ending with a double quote are treated in a special way:
  - The delimiting quote characters themselves are ignored.
  - The characters inside the quotes, including spaces, are taken as they are.
  - The only exception are the characters preceded by backslash. These are
    encoded as follows:
    - \" double quote
    - \\ backslash
    - \t tab
    - \n newline
- UXY format should not contain control characters, such as TABs.
  If there's a need for a TAB, use "\t" instead.

# Header

- First line of UXY format is the header.
- The format of the header line is identical to any other UXY line,
  however, its semantics differ.
- The value of a field in the header is the name of that particular column.
- The spacing of the fields in the header is a hint for the tools. They SHOULD
  try to align the data with the headers.

# Interactions between headers and records

- Fields SHOULD but don't have to be aligned with each other or with the
  headers.
- If there's less fields in a record than in the header the missing values
  are assumed to be empty strings.
- It's valid to for a record to have more fields than the header.
  The tools should consider the name of such column to be an empty string.

Example:

```
NAME  AGE ADDRESS
Alice 25  "Main Road 1, London" "Let's use this unnamed field for comments."
Bob   23  ""
Carol 55  "Hotel \"Excelsior\", New York"
```

# TOOLS

All UXY tools take input from stdin and write the result to stdout.

### uxy re

Reads the lines of the input and parses each one using the supplied regular
expression. Groups are then assigned to the fields specified in the header.

```
$ ls -l | uxy re "TIME NAME" ".* +(.*) +(.*)"
TIME NAME 
14:28 README.md
14:22 uxy
```

### uxy align

Aligns the data with the headers. This is done by resizing the columns so that even
the longest value fits into the column.

```
$ ls -l | uxy re "TIME NAME" ".* +(.*) +(.*)" | uxy align
TIME  NAME
14:36 README.md 
14:22 uxy
```

This command doesn't work with infinite streams.

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

### uxy from-json

Converts from JSON to uxy format.

```
$ cat test.json 
[
    {
        "Name": "Quasimodo",
        "Time": "14:30"
    },
    {
        "Name": "Moby Dick",
        "Time": "14:22"
    }
]
$ uxy from-json < test.json 
Name        Time
Quasimodo   14:30 
"Moby Dick" 14:22
```

### uxy to-json

Convers uxy table to JSON.

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


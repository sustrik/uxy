# UXY adds structure to the standard UNIX tools

Treating everything as a string is the way through which the great power and
verstatility of UNIX tools is achieved. However, sometimes the constant
parsing of strings gets a bit cumbersome.

UXY is a set of tools to manipulate UXY file format, which is a basically
a two-dimenstional table that's both human- and machine-readable.

# UXY file format

- First line is headers, separated by spaces.
- Each header is uppercase letters, digits and dashes.
  First character must be a letter.
- The spacing of headers SHOULD be used to determine the default widths of the
  fields. The fields that are not present in the header are assumed to have
  width of 10 characters.

- Remaining lines are data. There may be infinite amount of data items (pipe).
- Data line is composed of fields separated by arbitrary number spaces.
  In general the data SHOULD be aligned with headers whereever the fields
  actually fit in.
- Fields starting AND ending with a double quote are treated in a special way:
  - The quotes are ignored.
  - The characters inside the quotes including spaces are taken as is.
    The only exception are the characters preceded by backslash. These are
    decoded as follows:
    - \" double quote
    - \\ backslash
    - \t tab
    - \n newline
- Unquoted fields SHOULD NOT contain control characters, such as TABs.
  If they do the character MUST be treated as it was a question mark.

- Fields SHOULD but don't have to be aligned with each other or with the
  headers.
- If there's less fields in a record than in the header the missing values
  are assumed to be empty strings.
- If there are more fields in a record that there are in the header these
  are silently ignored.

Example:

```
NAME  AGE ADDRESS
Alice 25  "Main Road 1, London"
Bob   23  ""
Carol 55  "Hotel \"Excelsior\", New York"
```

# TOOLS

All tools take input from stdin and write the result to stdout.

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

This command doesn't work with infinite streams.

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

This command doesn't work with infinite streams.


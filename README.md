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
- The spacing of headers MAY be used to determine the default widths of the
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

All tools take input from stdin.
and write the result to stdout.

### uxy-in

Converts the input to UXY format.

Option -t specifies the format of the input stream (json, yml, xml, etc.)
Default is 'ssv' (space-separated values).

### uxy-out

Coverts the UXY-formatted input to a specified destination format.

Option -t specifies the format of the output stream (json, yml, xml, etc.)
Default is 'ssv' (space-separated values).

### uxy-pp

Pretty-print the data.

This command doesn't work with infinite streams.

Output:

```
NAME  AGE ADDRESS
---------------------------------------
Alice 25  Main Road 1, London
Bob   23
Carol 55  Hotel "Excelsior", New York
```

### uxy-ls

Same as `ls -l` except that the output is UXY-formatted.

TODO: Add other common POSIX tools.

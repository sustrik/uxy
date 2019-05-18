# UXY adds some amount of structure to the standard UNIX tools

# UXY file format

- First line is headers, separated by spaces.
- Each header is letters (case-insensitive), digits and dashes. First character must be a letter.
- Remaining lines are data.
- Data line is composed of fields separated by arbitrary number spaces.
- The fields support C escape sequnces plus:
  - \e - empty string (must by the only character in the field)
  - \m - missing field (must by the only character in the field)
  - \s - space

# TOOLS

All tools take input from stdin (can be redirected from file using -i option)
and write the result to stdout (can be redirected to file using -o option).

### uxy-in

Converts the input to UXY format.

Option -t specifies the format of the input stream (json, yml, xml, etc.)
Default is 'ssv' (space-separated values).

### uxy-out

Coverts the UXY-formatted input to a specified destination format.

Option -t specifies the format of the output stream (json, yml, xml, etc.)
Default is 'ssv' (space-separated values).

### uxy-fmt

Pretty-formats the input. The values are aligned with the column names.

This command doesn't work with infinite streams.

### uxy-filter

Filters an UXY stream.

- 1st positional arg: A list of output columns. The columns appear in the output
  in the order specified in this argument. A column specified as `foo=bar`
  will be renamed from `bar` to `foo`.
- `--filter` 

### uxy-grep

Same as grep except that the headers always go to the output.

If -n is specified, column `line` is added.

### uxy-ls

Same as `ls -l` except that the output is UXY-formatted.

TODO: Add other common POSIX tools.

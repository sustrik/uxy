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


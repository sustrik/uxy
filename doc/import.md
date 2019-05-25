# uxy import

Reads the lines of the input and parses each one using the supplied regular
expression. Matched groups are then assigned to the fields specified in
the header.

```
$ ls -l | uxy import "TIME NAME" ".* +(.*) +(.*)"
TIME NAME 
14:28 README.md
14:22 uxy
```

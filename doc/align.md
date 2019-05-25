# uxy align

Aligns the data with the headers. This is done by resizing the columns so that
even the longest value fits into the column.

```
$ ls -l | uxy import "TIME NAME" ".* +(.*) +(.*)" | uxy align
TIME  NAME
14:36 README.md 
14:22 uxy
```

This command doesn't work with infinite streams.

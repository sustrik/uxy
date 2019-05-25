# uxy grep

Field-based grep. If one argument is given it searches for the supplied regular
expression in any fields of the UXY input. If two arguments are given it
searches for the pattern in the specified field. Note that the pattern matching
works on decoded field values, not on the uxy greppresentation of the fields.
For example, for field "A B" A matches but "A does not. 

```
$ cat test.uxy 
NAME     SIZE 
README.md 8060 
test.csv 45
test.uxy 0
uxy      13458 
$ cat test.uxy | uxy grep csv
NAME     SIZE 
test.csv 45
$ cat test.uxy | uxy grep csv NAME
NAME     SIZE 
test.csv 45
$ cat test.uxy | uxy grep csv SIZE
NAME     SIZE
```

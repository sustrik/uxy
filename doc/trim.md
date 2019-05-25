# uxy trim

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


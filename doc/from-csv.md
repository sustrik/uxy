# uxy from-csv

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


# uxy from-json

Converts from JSON to UXY format.

```
$ cat test.json 
[
    {"Name": "Quasimodo", "Time": "14:30"},
    {"Name": "Moby Dick", "Time": "14:22"}
]
$ uxy from-json < test.json 
Name        Time
Quasimodo   14:30 
"Moby Dick" 14:22
```


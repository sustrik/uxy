# uxy to-json

Converts UXY format to JSON.

```
$ ls -l | uxy import "time name" ".* +(.*) +(.*)" | uxy to-json
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


# uxy to-json

Converts UXY format to JSON.

<pre>
<b>$ ls -l | uxy import "time name" ".* +(.*) +(.*)" | uxy to-json</b>
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
</pre>


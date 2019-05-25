# uxy from-json

Converts from JSON to UXY format.

<pre>
<b>$ cat test.json</b>
[
    {"Name": "Quasimodo", "Time": "14:30"},
    {"Name": "Moby Dick", "Time": "14:22"}
]
<b>$ uxy from-json < test.json</b>
Name        Time
Quasimodo   14:30 
"Moby Dick" 14:22
</pre>


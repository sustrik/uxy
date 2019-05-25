# uxy from-csv

Converts from CSV to UXY format.

<pre>
<b>$ cat test.csv</b>
NAME,TIME
Quasimodo,14:30
Moby Dick,14:22
<b>$ cat test.csv | uxy from-csv | uxy align</b>
NAME        TIME
Quasimodo   14:30 
"Moby Dick" 14:22 
</pre>


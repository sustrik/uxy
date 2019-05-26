# uxy grep

Field-based grep.

If one argument is given it searches for the supplied regular
expression in any fields of the UXY input.

<pre>
<b>$ uxy grep Moby < test.uxy</b>
</pre>

If two arguments are given it searches for the pattern in the specified field.

<pre>
<b>$ uxy grep Moby NAME < test.uxy</b>
</pre>

If many arguments are given they are treated as pairs of regular expressions
and field names. If there's an odd number of arguments the last one is matched
against all the fields.

<pre>
<b>$ uxy grep "^Moby.*$" NAME whale SPECIES < test.uxy</b>
</pre>

Note that the pattern matching works on decoded field values, not on the UXY
formatting of the fields. For example, if there is a field with value "A B"
it would be matched by regular expression `A` but not by `\"A`.

### Example

<pre>
<b>$ cat test.uxy</b>
NAME     SIZE 
README.md 8060 
test.csv 45
test.uxy 0
uxy      13458 
<b>$ cat test.uxy | uxy grep csv</b>
NAME     SIZE 
test.csv 45
<b>$ cat test.uxy | uxy grep csv NAME</b>
NAME     SIZE 
test.csv 45
<b>$ cat test.uxy | uxy grep csv SIZE</b>
NAME     SIZE
<b>$ cat test.uxy | uxy grep test NAME 45 SIZE</b>
NAME     SIZE 
test.csv 45
</pre>


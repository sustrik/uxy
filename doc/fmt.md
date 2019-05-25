# uxy fmt

Takes an UXY input and reformats it according to the supplied headers.

It allows for:

- reordering of columns
- resizing of columns
- dropping columns
- adding new columns

<pre>
<b>$ cat test.uxy</b>
TIME  NAME
15:03 README.md 
16:08 uxy
$ uxy fmt "NAME          TIME" < test.uxy 
NAME          TIME 
README.md     15:03 
uxy           16:08 
</pre>


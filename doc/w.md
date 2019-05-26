# uxy w

Wraps `w` tool and outputs the results in UXY format.

The output has following fields:

- **USER**
- **TTY**
- **FROM**
- **LOGIN**
- **IDLE**
- **JCPU**
- **PCPU**
- **WHAT**

### Example

<pre>
<b>$ uxy w</b>
USER     TTY    FROM    LOGIN    IDLE    JCPU    PCPU    WHAT 
martin   :0     :0      03May19  ?xdm?   1:08m   0.03s   "/usr/bin/foo --bar"
</pre>

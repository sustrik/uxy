# uxy ps

Wraps `ps` tool and outputs the results in UXY format.

The output has follwoing fields:

- **PID**
- **TTY**
- **TIME**
- **CMD**

When uxy is launched with `-l` option (`uxy -l ps`) following fields are added:

- **CONTEXT**
- **F**
- **S**
- **UID**
- **PPID**
- **C**
- **PRI**
- **NI**
- **ADDR**
- **SZ**
- **WCHAN**
- **RSS**
- **PSR**
- **STIME**

<pre>
<b>$ uxy ps</b>
PID      TTY      TIME       CMD 
4464     pts/0    00:00:01   bash 
23100    pts/0    00:00:00   python3 
23101    pts/0    00:00:00   ps
</pre>


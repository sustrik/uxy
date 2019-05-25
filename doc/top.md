# uxy top

Runs `top` tool in one-off manner and outputs the results in UXY format.

### Example

<pre>
<b>$ ./uxy top</b>
PID    USER     PR   NI   VIRT     RES      SHR      S CPU   MEM   TIME       COMMAND 
4529   martin   20   0    41924    3708     3144     R 18.8  0.0   0:00.03    top
1      root     20   0    225916   9640     6600     S 0.0   0.1   1:57.75    systemd 
2      root     20   0    0        0        0        S 0.0   0.0   0:00.52    kthreadd 
4      root     0    -20  0        0        0        I 0.0   0.0   0:00.00    kworker/0:0H 
6      root     0    -20  0        0        0        I 0.0   0.0   0:00.00    mm_percpu_wq
</pre>

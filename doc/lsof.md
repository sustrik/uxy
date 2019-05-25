# uxy lsof

Wraps `lsof` tool and outputs the results in UXY format.

<pre>
<b>$ uxy lsof</b>
COMMAND             PID    TID    USER           FD      TYPE    DEVICE             SIZEOFF   NODE       NAME
AudioIPC1           28097  28858  martin         mem     REG     259,2              5288      2236410    /var/cache/fontconfig/6afa.cache-7 
AudioIPC1           28097  28858  martin         mem     REG     259,2              2552      2228534    /var/cache/fontconfig/e0aa.cache-7 
AudioIPC1           28097  28858  martin         0r      CHR     1,3                0t0       6          /dev/null 
AudioIPC1           28097  28858  martin         1u      unix    0x0000000000000000 0t0       32328      type=STREAM 
AudioIPC1           28097  28858  martin         2u      unix    0x0000000000000000 0t0       32329      type=STREAM 
AudioIPC1           28097  28858  martin         3u      unix    0x0000000000000000 0t0       2115911    type=STREAM 
AudioIPC1           28097  28858  martin         4u      unix    0x0000000000000000 0t0       2062380    type=SEQPACKET 
AudioIPC1           28097  28858  martin         5u      unix    0x0000000000000000 0t0       2062383    type=SEQPACKET 
AudioIPC1           28097  28858  martin         6r      REG     0,24               276       3          "/dev/shm/org.chromium.SK1kmw (deleted)" 
AudioIPC1           28097  28858  martin         7w      FIFO    0,12               0t0       2115912    pipe 
AudioIPC1           28097  28858  martin         8r      FIFO    0,12               0t0       2113268    pipe 
AudioIPC1           28097  28858  martin         9u      sock    0,9                0t0       2116129    "protocol: UNIX" 
</pre>

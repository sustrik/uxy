# uxy ifconfig

Wraps `ifconfig` tool and outputs the results in UXY format.

The output has following fields:

- **NAME**
- **RX-PACKETS**
- **RX-BYTES**
- **RX-ERRORS**
- **RX-DROPPED**
- **TX-PACKETS**
- **TX-BYTES**
- **TX-ERRORS**
- **TX-DROPPED**
- **FLAGS**

When uxy is launched with `-l` option (`uxy -l ifconfig`) following fields are added:

- **INET-ADDR**
- **INET-NETMASK**
- **INET6-ADDR**
- **INET6-PREFIXLEN**
- **INET6-SCOPEID**
- **ETHER-ADDR**
- **MTU**
- **INTERRUPT**
- **MEMORY**
- **RX-OVERRUNS**
- **RX-FRAME**
- **TX-OVERRUNS**
- **TX-CARRIER**
- **TX-COLLISIONS**
- **TX-QUEUELEN**

### Example

<pre>
<b>$ uxy ifconfig</b>
NAME       RX-PACKETS RX-BYTES     RX-ERRORS RX-DROPPED TX-PACKETS TX-BYTES     TX-ERRORS TX-DROPPED FLAGS 
enp0s31f6  0          0            0         0          0          0            0         0          UP,BROADCAST,MULTICAST 
lo         35241      3074912      0         0          35241      3074912      0         0          UP,LOOPBACK,RUNNING 
wlp3s0     2451611    3383734099   0         0          862870     96392848     0         0          UP,BROADCAST,MULTICAST
</pre>


# [Over The Domain](https://hack.cert.pl/challenge/over-the-domain)

## Task

We get a PCAP dump with only DNS queries.

## Solution

After looking at the packets many of them had domains like `MFxFVgxdYDVfcnBJ.whatsapp.com`. and the first domain segment looked very much like base64.

So we can filter those packets and extract the zip file: [solve.py](./solve.py)

But for some reason the archive was corrupted, so I manually constructed the flag from fragments with the help of `strings data.zip`


```
=@ib3_s33n}
...
Y@+|qyC/%}Do|9sDHzAhK/Levu4{nC.rt&YDOxcG""mt_mean7_t0_b{th1s_w4s_n0{_;Ym vl7+9p
ecsc24
```


`ecsc24{th1s_w4s_n0t_mean7_t0_b3_s33n}`
# [S69](https://hack.cert.pl/challenge/s69)

## Task

We get a bugged website with reporting functionality. We have to access `/secret` to get the flag.

## Solve

A simple XSS in the `clientIp` field.

[Solve script](./solve.py)

`ecsc24{gotta_have_an_xss_challenge_right?}`
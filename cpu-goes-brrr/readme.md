# [CPU goes brrr](https://hack.cert.pl/challenge/brrr)

## Task

We are given a reaaaly slow executable which prints the flag.

## Research

Cleaned up decompiled code: [code.c](./code.c)

Shortened pseudocode of what it does:


```py
def get_xor_key(arg):
    x = find_first_prime_in_formula_with_index_larger_than(arg)
    x = ~x

    result = 0;
    for (i = 0; i < 8; i = i + 1) {
        n = 0;

        for (j = 0; j < 0xba04015; j = j + 1) {
            # random binary manipulation
            n = ...
            x = ...
        }

        result = result * 2 + n;
    }

    return result

flag = [
    data[i] ^ get_xor_key(i ** 3)
    for i in range(len(data))
]
```

where the formula is a recursive function `f(0) = f(1) = f(2) = 1`, `f(x) = f(x-1)+f(x-2)+f(x-3)`

## Solution

First, we have to optimize finding prime values of the recursive function:

```rs
fn find_primes_in_sequence(max_i: usize) -> Vec<(usize, i64)> {
    let mut sequence_primes = Vec::new();
    let mut sequence = VecDeque::from(vec![Wrapping(1), Wrapping(1), Wrapping(1)]);
    let mut i = 3;

    while i <= max_i {
        let next = sequence.iter().sum::<Wrapping<i64>>().0;

        sequence.push_back(Wrapping(next));
        sequence.pop_front();

        if is_prime(&(next as u64).to_string()) {
            sequence_primes.push((i, next));
            // println!("prime {}: {}", i, next)
        }

        if i > max_i {
            break;
        }

        i += 1;
    }

    sequence_primes
}
```

Then, we have to optimize the values with which the flag is xored. Initially there were too many iterations (8 * 0xba04015)

```c
int get_xor_key(undefined4 arg)
{
  x = find_prime_value_in_formula(arg);
  x = ~x;
  result = 0;
  for (i = 0; i < 8; i = i + 1) {
    n = 0;
    for (j = 0; j < 0xba04015; j = j + 1) {
      n = (ushort)(x >> 0xc ^ x >> 8 ^ x >> 10 ^ x >> 0xb) & 1;
      x = (ushort)(n << 0xf) | x >> 1;
    }
    result = result * 2 + n;
  }
  return result;
}
```

Using empirical methods I discovered that the values of `n` and `x` are repeating every 256 iterations of this fragment:

```
n = (ushort)(x >> 0xc ^ x >> 8 ^ x >> 10 ^ x >> 0xb) & 1;
x = (ushort)(n << 0xf) | x >> 1;
```

So `0xba04015` can be simplified to `0xba04015 % 256` and the result will remain the same.

<br>

[Solve script](./solve/src/main.rs)

`ecsc24{sl0w_4nd_5t3ady_w1ns_th3_r4ce}`
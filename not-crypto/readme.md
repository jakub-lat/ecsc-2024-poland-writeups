# [notCrypto](https://hack.cert.pl/challenge/notCrypto)

## Task

We are given some Java code and a netcat service.

The code reads the flag and then encrypts it using weird logic.

## Research

Because of the challenge name, we have to find a path in the code which generates the key deterministically based on the input.

This fragment seemed very interesting:
```
    private final Map<C, String> secrets = IntStream.range(Character.MIN_VALUE, Character.MAX_VALUE)
        .mapToObj(C::new)
        .collect(Collectors.toMap(
                Function.identity(),
                c -> UUID.randomUUID().toString()
        ));


    String generateRandomPassword(String userInput) {
        return userInput.chars()
                .mapToObj(i -> (char) i)
                .map(C::new)
                .map(secrets::get)
                .collect(Collectors.joining());
    }
```

Because of the `(char) i` cast.

From documentation:

```
String.chars() 
Returns a stream of int zero-extending the char values from this sequence. Any char which maps to a surrogate code point is passed through uninterpreted.
```

So String.chars() returns a list of ints! not chars - surrogates are not treated differently.

The `secrets` array contains values for chars from `\u0000` up to `\uffff`. If the input contains a character which maps to int value larger than `0xffff`, secrets::get will return null.

Given the seed `�����������`, generateRandomPassword will always return the same result - "null" * 11

Knowing the password for the encryption key, we can simply get the flag: [solve.java](./solve.java)

`ecsc24{integer_cache_and_2_byte_chars_#justjavathings}`
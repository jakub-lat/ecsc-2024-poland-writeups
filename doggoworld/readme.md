# [DoggoWorld](https://hack.cert.pl/challenge/doggoworld)

## Task

> We have put up the site with photos of the best dogs for those who are knowledgeable of HTTP standard. Can you get these pictures?

We are given a website, which initially throws an error telling that we should access it with `doggobrowser`.

## Solution

We have to access the website with appropriate HTTP headers, according to error messages.

Final script:

```sh
curl -v https://doggoworld.ecsc24.hack.cert.pl/ \
    -H "User-Agent: doggobrowser" \
    -H "X-Forwarded-For: 127.0.0.1" \
    -H "Accept-Language: en-US" \
    -H "Cookie: do_you_like_dogs_and_cats=YES" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "doggo=ZmxhZw==" > doggo.jpg
```
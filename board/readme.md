# [Board](https://hack.cert.pl/challenge/board)

## Task

We are given an onion website with a PHP image forum (TinyIB), and we have to access `/flag` to get the flag. But the route doesn't allow anonymous users.

## Research

By analyzing TinyIB [source code](https://gitlab.com/tslocum/tinyib), we can discover that a cool functionality is embed posting, which calls `file_get_contents()`. I thought that there has to be an LFI vuln of some kind.

Adding a post with embed=`file:///./inc/database/flatfile/.posts` gives an interesting error:

```
(...)
Warning: file_get_contents(file:///./inc/database/flatfile/.posts): Failed to open stream: No such file or directory in /var/www/html/ib/inc/functions.php on line 606
```

With that, we have the root directory of the web server - `/var/www/html/ib` - who would have expected :)


After more digging, I discovered that in order to read data using LFI, we have to bypass two things:

1. Mimetype restriction
2. Thumbnail creation, which deletes any encoded data in images

As it turns out, `php://filter` will be much of help in achieving it.

## Solution

Using [wrapwrap](https://github.com/ambionics/wrapwrap) we may construct an php://filter URL, which points to a corrupted PNG image, which has embedded another file accessed by the LFI vuln.

The image has to be corrupted, because then, the website will crash and reveal the original, not-thumbnailed image URL - `src/<randomized nam>.png`.

In `attachFile()` function, there is a code fragment:

```php
if (!createThumbnail($file_location, 'thumb/' . $post['thumb'], $thumb_maxwidth, $thumb_maxheight)) {
    @unlink($file_location);
    fancyDie(__('Could not create thumbnail.'));
}
```

Here, if `createThumbnail(...)` returns an error, the file will not be deletd. The thumbnail is created with GD Image Processing Library, and if the image is corrupted, it will throw an error.

So, using the embedded-image LFI, we can read the source code of the `/flag/` route, which as I guessed is located at `/var/www/html/flag/index.php`

[Solve script](./solve.py)

```sh
torsocks python3 solve.py /var/www/html/flag/index.php 3000
strings out.png
```

`ecsc24{GreetingsPeopleOfTheWorld-WeWereAnonymous}`
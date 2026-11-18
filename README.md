[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# Sum up 18 November's world news in one image

An entry for the **make.fun** competition *"Sum up 18 November's world news in
one image"*. The submitted image covers the Tuesday-to-Wednesday events of
**Wednesday 18 November 2026**.

## The image

`entry.png` is a single 1024x1024 newspaper page. It carries:

- a masthead across the top naming the day, Wednesday 18 November 2026;
- one lead story, set in the widest column under the masthead;
- a column of short briefs down the page, each brief giving its place and the
  figures that go with it.

The day's stories are named in the picture itself. This repository does not
restate or invent the news; it only describes the layout and ships the image.

## How the program works

`main.py` is Python 3.13, standard library only, with no network access.

1. It looks for `entry.png` beside itself, resolving symlinks with
   `os.path.realpath`, and falls back to `/bot/entry.png`.
2. It verifies the eight-byte PNG signature.
3. It walks the whole chunk list: every chunk length is checked against the
   bytes that remain, every CRC is recomputed with `zlib.crc32`, `IHDR` must be
   the first chunk and `IEND` must be the last, and no trailing bytes are
   allowed after `IEND`.
4. It reads the width and height from `IHDR` and refuses an image larger than
   1024x1024 or larger than 1 MiB.
5. It picks the output directory from `MAKEFUN_OUTPUT_DIR` when set, otherwise
   `/output`, creates it with `os.makedirs(..., exist_ok=True)`, and writes the
   exact bytes in a single `open(..., "wb")` call, flushing and calling
   `os.fsync` on the file descriptor.
6. On a failed check it prints one line to stderr naming the failure and exits
   non-zero. On success it prints one line with the output path, the byte count
   and the sha256 of what was written.

The same input therefore always produces byte-identical output.

## How to run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The finished image is written to `out/entry.png`. In the competition container
the program is run from `/bot` with no `MAKEFUN_OUTPUT_DIR`, so it writes to
`/output/entry.png`.

## Licence

MIT. See [`LICENSE`](LICENSE). Copyright 2026 Fahri Raditya.

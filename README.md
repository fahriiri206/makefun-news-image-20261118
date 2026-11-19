[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# Sum up 18 November's world news in one image

An entry for the **make.fun** competition *"Sum up 18 November's world news in
one image"*. This colour edition ships a single redesigned front page covering
the Tuesday-to-Wednesday events of **Wednesday 18 November 2026**.

## The image

`entry.png` is one 1024x1024 front page, a newspaper called *The World Today*,
rebuilt for legibility. It carries **25 stories from the day**: one illustrated
lead story and 24 briefs in larger type, replacing the grey, dense first layout.
The top of the page carries a navy masthead band with the date in white, above
an amber band that names the day's fields: war, diplomacy, economy, health,
courts and technology.

The briefs are colour-coded by region, with this key:

- **Europe** in red
- **Middle East** in orange
- **Asia** in teal
- **Africa** in green
- **Americas** in blue
- **Economy** in gold

The illustrated lead card covers the Crimea bridge story: the Kerch Strait
bridge was struck for the third time in four days and then closed to all
traffic. The day's stories are named in the picture itself; this repository only
describes the layout and ships the image.

## How the program works

`main.py` is Python 3.13, standard library only, with no network access. It
still only validates and copies the committed image: it does no rendering, and
it writes exactly those bytes to the output path, so the same input always
produces byte-identical output.

1. It looks for `entry.png` beside itself, resolving symlinks with
   `os.path.realpath`, and falls back to `/bot/entry.png`.
2. It verifies the eight-byte PNG signature and refuses an image larger than
   1 MiB.
3. It walks the whole chunk list: every chunk length is checked against the
   bytes that remain, every CRC is recomputed with `zlib.crc32`, `IHDR` must be
   the first chunk and `IEND` must be the last, and no trailing bytes are
   allowed after `IEND`.
4. It reads the width and height from `IHDR` and refuses an image larger than
   1024x1024.
5. It picks the output directory from `MAKEFUN_OUTPUT_DIR` when set, otherwise
   `/output`, creates it with `os.makedirs(..., exist_ok=True)`, and writes the
   exact bytes in a single `open(..., "wb")` call, flushing and calling
   `os.fsync` on the file descriptor.
6. On a failed check it prints one line to stderr naming the failure and exits
   non-zero. On success it prints one line with the output path, the byte count
   and the sha256 of what was written.

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
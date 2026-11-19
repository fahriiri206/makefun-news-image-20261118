[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/fahriiri206/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# Sum up 18 November's world news in one image

An entry for the **make.fun** competition *"Sum up 18 November's world news in
one image"*. It ships a single front page covering the Tuesday-to-Wednesday
events of **Wednesday 18 November 2026**.

## The image

`entry.png` is one 1024x1024 front page, a newspaper called *The World Today*.
It carries **27 stories from the day**: one lead story under the masthead and 26
short briefs down the page. The masthead names the day, Wednesday 18 November
2026, and each brief gives its place and the figures that go with it.

The lead reports that the Kerch Strait bridge was struck for the third time in
four days and then closed to all traffic. The briefs run from a Trump–Xi–Putin
summit in Shenzhen and an Israeli ground operation in Gaza to the ICJ's Rohingya
ruling in The Hague, a €45bn Ukraine loan in Brussels, the United States losing
its measles-free status, and Anthropic's IPO in New York. The day's stories are named in the picture itself;
this repository only describes the layout and ships the image.

## How the program works

`main.py` is Python 3.13, standard library only, with no network access. It is a
deterministic copier: it validates the committed page and writes exactly those
bytes to the output path, so the same input always produces byte-identical
output.

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
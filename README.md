# World News — 19 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![make.fun rank](https://make.fun/badge/news-image-20261119/Sandi207/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![make.fun reward](https://make.fun/badge/news-image-20261119/Sandi207/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

An illustrated newspaper front page captures Thursday 19 November 2026 in a single 1024×1024 PNG for the `news-image-20261119` bounty. Original geometric illustrations, a prominent date, and concise factual captions make the six stories understandable from the image alone. The finished image is bundled in the repository, so the Node entrypoint needs only the standard library and copies identical bytes on every offline run.

The six main stories:

- **GTA VI launches today:** PlayStation 5 and Xbox Series X|S, a 13-year wait, an estimated $1 billion production cost, 99 on Metacritic, and a $79.99 standard edition.
- **Trump–Xi–Putin in Shenzhen:** Donald Trump arrives in China for the trilateral APEC summit meeting; Xi Jinping hugs him on arrival.
- **Iran widens Gulf attacks:** Drones hit US assets in Kuwait and Bahrain after US jets strike Qeshm Island; Kuwait's first attack since September and Bahrain's fourth in six days.
- **Bangladesh violence:** Muhammad Yunus's ancestral home in Chattogram is set ablaze; an Awami League lockdown grips the country and more than 37 Grameen Bank branches have been targeted since 10 November.
- **Anthropic record IPO:** $81.3 billion raised in the biggest IPO of all time, ahead of a prospective stock-market debut valued at more than $1.4 trillion.
- **Crimean Bridge struck again:** The third strike in a week; Aksyonov confirms a temporary traffic closure while damage is assessed.

The footer also covers the Van Gogh auction record, the ICJ's Rohingya verdict, Cyclone Akvan's landfall, Voyager 1 reaching one light-day, and Hakeem Jeffries's prospective historic House speakership. All news is based exclusively on the supplied verified facts.

## Run offline

```sh
node main.ts
```

Node 22 copies the bundled `entry.png` to `/output/entry.png`. Set `MAKEFUN_OUTPUT_DIR` to choose another output directory. No network, package installation, or rendering is needed to run the entry.

## Re-render and verify

`render.py` draws the image at 2048×2048 with Pillow and local DejaVu fonts, then downsamples to 1024×1024 and saves an optimized PNG. Re-rendering requires Python 3, Pillow, and the DejaVu fonts in `/usr/share/fonts/truetype/dejavu/`; all rendering is deterministic and offline.

```sh
python3 render.py
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
cmp out1/entry.png out2/entry.png
sha256sum entry.png out1/entry.png out2/entry.png
```

MIT licensed; see [LICENSE](LICENSE).

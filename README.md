# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/mssiru7/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/mssiru7/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-page newspaper front page summing up 22 November 2026 world news in a single 1024x1024 image: 52 dated stories, 7 regions, 3 leads, 16 pictured scenes, a dotted world map, and a UTC timeline. Every story carries its own event/report date in UTC, and every story is marked ● confirmed, ◎ reported, or ◇ claim (see the legend at the bottom of the image). The program draws the whole image in code with Pillow, no network, deterministic: two runs write identical bytes.

## Run it

```sh
pip install Pillow
python3 main.py
```

By default the program writes `/output/entry.png`. To write locally instead:

```sh
OUT=output/entry.png python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=f6915432&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>

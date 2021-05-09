# The asvz bot

This repo contains a script to automatically enroll to ASVZ lessons

## Features

- Enroll to lesson
  - based on lesson ID (for lessons visited once)
  - based on sport ID, day, time, trainer, facility (for lessons visited periodically)
- Enroll to lesson that is already full
- Login as a member of
  - ETH
  - UZH
  - ZHAW
- Save your credentials locally and reuse them on the next run

## Run

### Prerequisites

You need to install the following:

- [Python 3](https://www.python.org/downloads/)
- [Chrome](https://support.google.com/chrome/answer/95346) or [Chromium](https://www.chromium.org/getting-involved/download-chromium)

You **must not** run the script >24h before the enrollement opens.

### First time

```bash
cd src
python3 -m pip install venv
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 asvz_bot.py -h
```

### After the first time

```bash
cd src
source .venv/bin/activate
python3 asvz_bot.py -h
```

### Examples

Enroll by lesson ID and save credentials (locally in `.asvz-bot.json`)

```bash
python3 asvz_bot.py lesson --organisation "ETH" --username "flbuetle" --save-credentials 196346
```

Enroll by lesson ID and use saved credentials

```bash
python3 asvz_bot.py lesson 196346
```

Enroll by lesson attributes

```bash
python3 asvz_bot.py training --weekday "Mo" --start-time "18:15" --trainer "Karin Hollenstein" --facility "Sport Center Hönggerberg" 45743
```

## Development

### Script

TODO

### Mock

```bash
cd mock
docker-compose up --build
```

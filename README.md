# The asvz bot

This repo contains a script to automatically enroll to ASVZ lessons

## Features

- Enroll to lesson
  - based on lesson ID (for lessons visited once)
  - based on sport ID, day, time, trainer, level, facility (for lessons visited periodically)
- Enroll to lesson that is already full
- Login as a member of
  - ETH
  - UZH
  - ZHAW
  - PHZH
  - ASVZ
- Save your credentials locally and reuse them on the next run
- Note: 
    UZH, ZHAW and PHZH use SWITCH edu-ID as login (*email* + password).
    ETH uses own login (*nethz* + password)
    ASVZ uses own login (*ASVZ-ID* + password)

## Run

### Prerequisites

You need to install the following:

- [Python 3](https://www.python.org/downloads/)
- [Chrome](https://support.google.com/chrome/answer/95346) or [Chromium](https://www.chromium.org/getting-involved/download-chromium)

### First time

```bash
cd src
python3 -m pip install virtualenv
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
python3 asvz_bot.py --organisation "ETH" --username "flbuetle" --save-credentials lesson 196346
```

Enroll by lesson ID and use saved credentials

```bash
python3 asvz_bot.py lesson 196346
```

Enroll by lesson attributes and use saved credentials

```bash
python3 asvz_bot.py training \
  --weekday "Mo" \
  --start-time "18:15" \
  --trainer "Karin Hollenstein" \
  --level "Fortgeschrittene" \
  --facility "Sport Center Hönggerberg" \
  45743
```

## Docker
In order to run the script using docker, follow these two steps:

1. Install docker and docker compose (usually included) as explained on the official docker [website](https://docs.docker.com/engine/install/).

2. Build the image using the following command from the repository's base directory:
    ```bash
    docker build
    ```
    This should show you the asvz-bot usage documentation

3. Run your command using the following command:
    ```bash
    docker run asvz-bot {command}
    ```
    where `command` is the same command you would usually pass to your local installation, including `python3 asvz-bot.py`.

// TODO: Support `.env` file based configuration

## Development

### Script

TODO

### Mock

```bash
cd mock
docker-compose up --build
```

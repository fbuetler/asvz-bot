## :warning: **asvz bot is no longer maintained**

This repository has been archived on Dec 18th, 2023.

The ASVZ IT department has kindly asked me to discontinue this project in compliance with their [Fair Play Rules](https://asvz.ch/59666-willkommen-im-asvz#details1-fold-5492-0).

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

2. Configure event parameters in the `env` file. Provide the required values as described above or on the cli help. Make sure to comment out or remove any lines for values you are not using. 

3. Build the image using the following command from the repository's base directory:
   ```bash
   docker compose --env-file env up --build
   ```

It is possible to configure multiple `env` files for different recurring events and start the bot with the appropriate one by specifying the `--env-file`
flag as follows:

1. Copy the `env` file and name it after your desired event, using one of the following patterns: `myEvent.env` or `myEvent-env`
2. Run the bot using the following command, where you replace the file name with your actual file name:
    ```bash
    docker compose --env-file myEvent.env up --build
    ```

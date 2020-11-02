## The asvz bot

This repo contains a ansible role to setup the asvz bot

### How to use the script only

**Note**: You need to have python3, python3-pip and chromium-chromedriver (or chromium) installed. You must not run the script >24h before the enrollement opens.

```bash
cd files
python3 -m pip install venv
python3 -m venv .venv
source .venv/bin/activate
python3 install -r requirements.txt
python3 asvz_bot.py -h
```



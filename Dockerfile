FROM continuumio/miniconda3:latest

ENV QTWEBENGINE_DISABLE_SANDBOX=1
ENV DISPLAY=:99

# Install latest chromium release
RUN apt -y update && apt -y install chromium

# Headless Workaround
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y xorg xvfb gtk2-engines-pixbuf dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

# Copy source files & install dependencies
COPY src/requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY src .

CMD ["bash", "-c", "Xvfb -ac :99 -screen 0 1280x1024x16 & python3 asvz_bot.py"]

# DEBUG Commands
# User command: \"$@\"
# CMD ["python3", "asvz_bot.py", "-h"]
# CMD ["tail", "-f", "/dev/null"]

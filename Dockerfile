FROM ubuntu:zesty

RUN apt-get update && apt-get install --yes python python-pip

RUN apt-get update && apt-get install --yes python-tk imagemagick ffmpeg
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD cd yndx-astana-demo-bot && ./bot.py


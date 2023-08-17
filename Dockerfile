FROM python:3.8-slim

RUN apt-get update -qq 
RUN apt-get install ffmpeg -y

RUN python3.8 -m venv env
RUN . env/bin/activate

ADD requirements.txt /
RUN python -m pip install -r requirements.txt
RUN rm requirements.txt

COPY . /lyrics-to-text
WORKDIR /lyrics-to-text

CMD ["python", "main.py"]

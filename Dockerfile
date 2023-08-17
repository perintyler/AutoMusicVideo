FROM python:3.8.16-slim

RUN python3.8 -m venv env
RUN . env/bin/activate
ADD requirements.txt /
RUN python -m pip install -r requirements.txt
RUN rm requirements.txt

RUN apt-get update -qq && apt-get install ffmpeg -y

COPY . /lyrics-to-text
WORKDIR /lyrics-to-text

CMD ["python", "main.py"]

FROM python:3.8.16-slim

WORKDIR /lyrics-to-text
COPY . /lyrics-to-text

RUN apt-get update -qq && apt-get install ffmpeg -y
RUN python -m pip install —upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["python3", "main.py"]

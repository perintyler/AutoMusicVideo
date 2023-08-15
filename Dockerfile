# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.8.16
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1


ADD requirements.txt /

RUN python -m pip install -r requirements.txt

ADD audio.py /
ADD main.py /
ADD lyrics.py /
ADD music_video.py /
ADD text_to_image.py /
ADD config.py /

ADD config.json /

COPY songs .

CMD ["python" , "main.py"]

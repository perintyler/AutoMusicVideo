
################# set the base image #################

FROM python:3.8-slim

################# install dependencies #################

# set up a python virtual enviroment
RUN python3.8 -m venv env
RUN . env/bin/activate

# https://stackoverflow.com/questions/68673221/warning-running-pip-as-the-root-user
ENV PIP_ROOT_USER_ACTION=ignore

# install pip packages listed in requirements file
RUN python -m pip install --upgrade pip
ADD requirements.txt /
RUN python -m pip install -r requirements.txt
RUN rm requirements.txt

# install ffmpeg with apt-get
RUN apt-get update -qq 
RUN apt-get install ffmpeg -y

################# copy source files #################

COPY . /lyrics-to-text
WORKDIR /lyrics-to-text

################# define entry point command #################

CMD ["python", "main.py"]

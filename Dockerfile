
################# set the base image #################

FROM python:3.11-slim

################# copy source files #################


COPY ./storyboard /storyboard

RUN ls -R /storyboard

WORKDIR /AutoMusicVideo

################# setup enviroment #################

RUN python3.11 -m venv env
RUN . env/bin/activate

# https://stackoverflow.com/questions/68673221/warning-running-pip-as-the-root-user
ENV PIP_ROOT_USER_ACTION=ignore

################# install dependencies #################

# install pip packages listed in requirements file
RUN python -m pip install --upgrade pip
RUN python -m pip install /storyboard

# install ffmpeg with apt-get
RUN apt-get update -qq 
RUN apt-get install ffmpeg -y


################# define entry point command #################

# COPY ./run_locally.py /AutoMusicVideo
# CMD ["python", "run_locally.py"]

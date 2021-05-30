FROM python:3.7
#FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install x11-xserver-utils -y
RUN apt-get install -y libmtdev-dev
RUN apt-get install libglu1-mesa-dev -y
RUN apt-get install -qqy x11-apps

RUN adduser --disabled-password worker

USER worker
WORKDIR /home/worker

RUN mkdir app
COPY . app 


RUN pip install --user -r  app/requirements.txt 
RUN python .local/bin/garden install mapview
WORKDIR /home/worker/app
RUN mkdir bookmarks
RUN chmod 777 bookmarks
CMD python main.py start

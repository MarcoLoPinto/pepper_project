# Use the official Ubuntu 20.04 image as the base image
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# Set the working directory to /
WORKDIR /

# Install Python 3.10 and the required dependencies
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y && add-apt-repository universe -y
RUN apt-get install -y python3.10 python3-pip python3-eventlet
# RUN pip3 install --upgrade pip
RUN pip3 install Flask
RUN pip3 install cmake
RUN pip3 install dlib==19.22
RUN pip3 install opencv-python
RUN pip3 install face_recognition
RUN pip3 install pyopenssl
RUN pip3 install websocket-server

# Set the default command to run when the container starts
ADD init.bash /init.bash
RUN chmod +x /init.bash

CMD [ "bash", "-ci", "/init.bash" ]
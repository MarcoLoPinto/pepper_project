#!/bin/bash

# Set the port number to 5000 by default
port=5000

# Check if a port number was provided as a command-line parameter
if [ $# -gt 0 ]; then
    port=$1
fi

IMAGENAME=hri_server_image

VERSION=latest

# change setings here if needed
ROOT_PROJECT=$(pwd)/..
CAMERA_DEVICE=/dev/video0
PEPPER_TOOLS_HOME=$ROOT_PROJECT/src/Pepper/pepper_tools
PLAYGROUND_FOLDER=$ROOT_PROJECT/playground


echo "Running image $IMAGENAME:$VERSION ..."

if [ -f $CAMERA_DEVICE ]; then
  echo "Camera device $CAMERA_DEVICE enabled"
  CAMERA_DEVICE_STR="--device=$CAMERA_DEVICE"
fi

if [ -d /run/user/$(id -u)/pulse ]; then
  AUDIO_STR="--device=/dev/snd \
           -v /run/user/$(id -u)/pulse:/run/user/1000/pulse \
           -v $HOME/.config/pulse/cookie:/opt/config/pulse/cookie"
  echo "Audio support enabled"
fi

chmod go+rw ~/.config/pulse/cookie # this file needed by docker user


docker run -it \
    --name hri_server --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v $HOME/.Xauthority:/.Xauthority:rw \
    -e DISPLAY=$DISPLAY \
    --privileged \
    --net=host \
    $CAMERA_DEVICE_STR \
    $AUDIO_STR \
    -v $PLAYGROUND_FOLDER:/playground \
    -v $PEPPER_TOOLS_HOME:/src/pepper_tools \
    -v $HOME/.qibullet:/.qibullet \
    $IMAGENAME:$VERSION



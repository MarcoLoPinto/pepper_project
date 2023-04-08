import os, sys
import qi

# IP address and port of the Naoqi robot
robot_ip = "192.168.1.35"
robot_port = "9559"
connection_url = "tcp://" + robot_ip + ":" + robot_port

def say_test():
    tts_service.setParameter("speed",10)
    tts_service.say("Hello Marco!")

def motion_test():
    joint_names = ["HeadYaw", "HeadPitch"]
    angles = [0, -1.6]
    times = [5.0, 5.0]
    isAbsolute = True
    motion_service.angleInterpolation(joint_names, angles, times, isAbsolute)

def say_animated_test():
    configuration = {"bodyLanguageMode": "contextual"}
    animated_speech_service.say("Hello, I am Pepper the robot.",configuration)

def say_animated_test_2():
    anim = "animations/Stand/Gestures/Desperate_1"
    animated_speech_service.say("Hello! ^start("+anim+") Nice to meet you!")

try:
    app = qi.Application(["Module name", "--qi-url="+connection_url])
    print("Connected to the Naoqi robot at " + connection_url)

except Exception as e:
    print("Could not connect to the Naoqi robot on " + connection_url)
    print(str(e))
    
# Control code...

app.start() # start the session

posture_service = app.session.service("ALRobotPosture")
tts_service = app.session.service("ALTextToSpeech")
motion_service = app.session.service("ALMotion")
animated_speech_service = app.session.service("ALAnimatedSpeech")
tablet_service = app.session.service("ALTabletService")

posture_service.goToPosture("Stand", 1.0)

app.stop()
app.run() # blocking function, will exit when the connection is over / process is stopped
    





import os, sys
import qi
from naoqi import ALProxy
import math
import time

import threading

from PIL import Image
import io
import base64
import socket

class PepperBot:
    def __init__(self, ip, port = 9559, alive = False):
        self._colors = {"RED": "\033[1;31m", "BLUE": "\033[1;34m", "CYAN": "\033[1;36m", "GREEN": "\033[0;32m", "RESET": "\033[0;0m","BOLD": "\033[;1m", "REVERSE": "\033[;7m"}
        self._init_robot()
        self.connect(ip, port, alive)

    def _init_robot(self):
        self.ip = None
        self.port = None
        self.services = None

        self.stopSensorThread() # self.sensorThread = None
        self.sensorHeadTouch = 0.0
        self.sensorHandLeftTouch = 0.0
        self.sensorHandRightTouch = 0.0
        self.sensorSonarFront = 0.0
        self.sensorSonarBack = 0.0
        self.sensorFrontLaserDistance = 0.0

        self.stopFaceDetectionEvent()

        self.laserThread = None # TODO, or not


    def connect(self, ip="127.0.0.1", port=9559, alive=False):
        self.ip = ip
        self.port = port

        self._log_info("Starting services...")

        self.services = {}
        services = {
            'ALMemory':'ALMemory',
            'ALMotion':'ALMotion',
            'ALTextToSpeech':'ALTextToSpeech',
            'ALAnimatedSpeech':'ALAnimatedSpeech',
            'ALLeds':'ALLeds',
            'ALSpeechRecognition':'ALSpeechRecognition',
            'ALTabletService':'ALTabletService',
            'ALTouch':'ALTouch',
            'ALAnimationPlayer':'ALAnimationPlayer',
            'ALBehaviorManager':'ALBehaviorManager',
            'ALAutonomousLife':'ALAutonomousLife',
            'ALRobotPosture':'ALRobotPosture',
            'ALBackgroundMovement':'ALBackgroundMovement',
            'ALBasicAwareness':'ALBasicAwareness',
            'ALSpeakingMovement':'ALSpeakingMovement',
            'ALAudioRecorder':'ALAudioRecorder',
            'ALAudioDevice':'ALAudioDevice',
            'ALBattery':'ALBattery',
            'ALPeoplePerception':'ALPeoplePerception',
            'ALFaceDetection': 'ALFaceDetection'
        }
        not_activated_services = []
        for n,s in services.items():
            try:
                # self.services[n] = self.app.session.service(s)
                self.services[n] = ALProxy(s, self.ip, self.port)
            except Exception as e:
                not_activated_services.append(n)
                self.services[n] = None

        if len(not_activated_services) == len(services):
            self._log_error("%sThe robot is offline! (check ip and port)%s" %(self._colors['RED'], self._colors['RESET']))
        elif len(not_activated_services) > 0:
            self._log_warn("Services not activated: %s%s%s" %(self._colors['BOLD'],', '.join(not_activated_services),self._colors['RESET']))
        else:
            self._log_success("All services activated!")

        self.setAliveBehaviour(alive=alive)

    def quit(self):
        self._log_info("Quitting robot...")
        self._init_robot()
        self._log_info("Quitted robot.")

    # ---------------------- alive behaviour -----------------------------

    def setAliveBehaviour(self, alive = True):
        notSetted = []
        aliveServices = ['ALBackgroundMovement', 'ALBasicAwareness', 'ALSpeakingMovement']
        for aliveService in aliveServices:
            if self.services[aliveService] != None:
                self.services[aliveService].setEnabled(alive)
            else:
                notSetted.append(aliveService)
        
        if len(notSetted) == 0:
            self._log_info("All alive services are set to %s." %(str(alive)))
        elif len(notSetted) == len(aliveServices):
            self._log_error("All alive services cannot be enabled/disabled: %s" %((', ').join(notSetted)))
        else:
            self._log_error("Some alive services cannot be enabled/disabled: %s" %((', ').join(notSetted)))

    # ---------------------- non-blocking miscellaneous -----------------------------

    def waitForThread(self, thread_ref, service):
        if self.services[service] != None:
            self.services[service].wait(thread_ref, 0)
        else:
            self._log_error("Service %s not activated!" %(service))

    # ---------------------- speak and/or movement -----------------------------

    def say(self, text, speed = 60, blocking = True):
        service = 'ALTextToSpeech'
        if self.services[service] != None:
            self.services[service].setParameter("speed", speed)
            if blocking:
                self.services[service].say(text)
                return None
            else:
                threadService = self.services[service].post.say(text)
                return threadService
        else:
            self._log_error("Service %s not activated!" %(service))

    def angleInterpolation(self, names, keys, times, isAbsolute, blocking = True):
        service = 'ALMotion'
        if self.services[service] != None:
            if blocking:
                self.services[service].angleInterpolation(names, keys, times, isAbsolute)
                return None
            else:
                threadService = self.services[service].post.angleInterpolation(names, keys, times, isAbsolute)
                return threadService
        else:
            self._log_error("Service %s not activated!" %(service))

    def stand(self, blocking = True):
        service = 'ALRobotPosture'
        if self.services[service] != None:
            if blocking:
                self.services[service].goToPosture("Stand", 1.0)
                return None
            else:
                threadService = self.services[service].post.goToPosture("Stand", 1.0)
                return threadService
        else:
            self._log_error("Service %s not activated!" %(service))

    # ------------------------------ eyes colors ----------------------------------

    def eyesColors(self, r=0,g=0,b=0, duration = -1, part = 'Both'):
        service = 'ALLeds'
        colors = [('Red',r),('Green',g),('Blue',b)]
        if self.services[service] != None:
            ledId = "FaceLeds"
            if part == 'Left' or part == 'Right':
                ledId = part + ledId
            if duration > 0:
                self.services[service].fadeRGB(ledId, r,g,b, duration)
            else:
                for (color, isOn) in colors:
                    ledIdColor = ledId + color
                    if isOn:
                        self.services[service].on(ledIdColor)
                    else: 
                        self.services[service].off(ledIdColor)
        else:
            self._log_error("Service %s not activated!" %(service))

    def eyesWhite(self):
        service = 'ALLeds'
        if self.services[service] != None:
            self.services[service].on('FaceLeds')
        else:
            self._log_error("Service %s not activated!" %(service))

    def eyesGreen(self, duration = -1):
        self.eyesColors(0,1,0, duration)

    def eyesRed(self, duration = -1):
        self.eyesColors(1,0,0, duration)

    def eyesBlue(self, duration = -1):
        self.eyesColors(0,0,1, duration)
        
    # ---------------------------- console logging --------------------------------
    
    def _log_general(self,name,color,*args):
        print("%s[%s]%s %s" %(self._colors[color],name,self._colors['RESET'],str(args[0])))
        if len(args) > 1:
            print(args[1:])
    def _log_error(self,*args):
        self._log_general('ERROR','RED',*args)
    def _log_info(self,*args):
        self._log_general('INFO','RESET',*args)
    def _log_warn(self,*args):
        self._log_general('WARN','CYAN',*args)
    def _log_success(self,*args):
        self._log_general('SUCCESS','GREEN',*args)

    # ------------------- sensors (sonar, touch, laser) --------------------------

    def startSensorThread(self):
        if self.sensorThread == None:
            self.sensorThread = threading.Thread(target=self._sensorThread, args=(self,))
            self.sensorThread.start()

    def stopSensorThread(self):
        if hasattr(self, 'sensorThread') and hasattr(self.sensorThread, 'do_run'):
            self.sensorThread.do_run = False
        self.sensorThread = None

    def _sensorThread(self):
        service = 'ALMemory'
        if self.services[service] == None:
            self._log_error("Service %s not activated! sensorThread cannot start!" %(service))
            return

        sonarValues = ["Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value",
            "Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"]
        headTouchValue = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
        handTouchValues = ["Device/SubDeviceList/LHand/Touch/Back/Sensor/Value",
            "Device/SubDeviceList/RHand/Touch/Back/Sensor/Value"]
        frontLaserValues = [ 
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/X/Sensor/Value",
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg07/Y/Sensor/Value",
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/X/Sensor/Value",
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg08/Y/Sensor/Value",
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/X/Sensor/Value",
            "Device/SubDeviceList/Platform/LaserSensor/Front/Horizontal/Seg09/Y/Sensor/Value"]
    
        t = threading.currentThread()

        while getattr(t, "do_run", True):
            self.sensorHeadTouch = self.services[service].getData(headTouchValue)
            [self.sensorHandLeftTouch, self.sensorHandRightTouch] = self.services[service].getListData(handTouchValues)
            [self.sensorSonarFront, self.sensorSonarBack] = self.services[service].getListData(sonarValues)
            sensorFrontLaserValues = self.services[service].getListData(frontLaserValues)
            dd = 0 # average distance
            c = 0
            for i in range(0,len(sensorFrontLaserValues),2):
                px = sensorFrontLaserValues[i] if sensorFrontLaserValues[i] is not None else 10
                py = sensorFrontLaserValues[i+1] if sensorFrontLaserValues[i+1] is not None else 0
                d = math.sqrt(px*px+py*py)
                if d < 10:
                    dd = dd + d
                    c = c+1
            
            self.sensorFrontLaserDistance = dd / c if c>0 else 10.0

            time.sleep(0.2)

    # ------------------- face tracking, detection... --------------------------

    def onFaceDetected(self, value):
        faceID = -1

        if value == []: # empty value when the face disappears
            self.faceRecognized = False
        elif not self.faceRecognized: # only the first time a face appears
            self.faceRecognized = True

            facetimeStamp = value[0]
            faceInfoArray = value[1]

            for j in range( len(faceInfoArray)-1 ):

                faceInfo = faceInfoArray[j]
                faceShapeInfo = faceInfo[0]
                faceExtraInfo = faceInfo[1]
                faceID = faceExtraInfo[0]

        if self.services['ALVideoDevice'] != None and faceID>=0 and faceID not in self.facesSaved:
            self._log_info("New face detected, face id: %s, saved faces: %s" %(faceID, (', ').join(self.facesSaved))) # TODO remove after test
            fname = "face_%09d.png" %faceID
            if self.saveCameraImage(fname) == None:
                self._log_error("Cannot save face image from onFaceDetected callback!")
            self.facesSaved.append(faceID)

    def stopFaceDetectionEvent(self):
        if hasattr(self, 'faceDetectionId') and self.faceDetectionId != None:
            self.faceDetectionSubscriber.signal.disconnect(self.faceDetectionId)
        self.faceDetectionId = None
        self.stopVideoFrameGrabberEvent()
        self.faceRecognized = False
        self.faceDetectionIsActive = False

    def startFaceDetectionEvent(self):
        if self.robotCameraEvent != None: return
        self.startVideoFrameGrabberEvent() # connect to camera

        self.faceDetectionSubscriber = self.services['ALMemory'].subscriber("FaceDetected")
        self.faceDetectionId = self.faceDetectionSubscriber.signal.connect(self.onFaceDetected)
        self.faceRecognized = False
        self.facesSaved = []
        self.faceDetectionIsActive = True

    def stopVideoFrameGrabberEvent(self):
        service = 'ALVideoDevice'
        if self.services == None or self.services[service] == None: return
        if hasattr(self, 'robotCameraEvent') and self.robotCameraEvent != None:
            self.services[service].unsubscribe(self.robotCameraEvent)
        self.robotCameraEvent = None

    def startVideoFrameGrabberEvent(self):
        service = 'ALVideoDevice'
        if self.services[service] == None:
            self._log_error("Service %s not activated! startVideoFrameGrabberEvent cannot start!" %(service))
            return
        if self.robotCameraEvent != None:
            self._log_error("The startVideoFrameGrabberEvent already started!")
            return
        resolution = 2    # VGA
        colorSpace = 11   # RGB
        self.robotCameraEvent = self.services[service].subscribeCamera("grab3_images", 0, resolution, colorSpace, 5)

    def getCameraImage(self):
        if not hasattr(self, 'robotCameraEvent') or self.robotCameraEvent == None:
            self._log_error("The startVideoFrameGrabberEvent was never called! Start it first!")
            return None

        img = self.services['ALVideoDevice'].getImageRemote(self.robotCameraEvent)
        if img is None:
            self._log_error("Cannot get the image from the startVideoFrameGrabberEvent!")
            return None
        
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)
        return imx
    
    def getCameraImageArray(self):
        if not hasattr(self, 'robotCameraEvent') or self.robotCameraEvent == None:
            self._log_error("The startVideoFrameGrabberEvent was never called! Start it first!")
            return None

        img = self.services['ALVideoDevice'].getImageRemote(self.robotCameraEvent)
        if img is None:
            self._log_error("Cannot get the image from the startVideoFrameGrabberEvent!")
            return None
        
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        return imageArray, (imageWidth, imageHeight)
    
    def getCameraImageBase64(self):
        if not hasattr(self, 'robotCameraEvent') or self.robotCameraEvent == None:
            self._log_error("The startVideoFrameGrabberEvent was never called! Start it first!")
            return None

        img = self.services['ALVideoDevice'].getImageRemote(self.robotCameraEvent)
        if img is None:
            self._log_error("Cannot get the image from the startVideoFrameGrabberEvent!")
            return None
        
        imageWidth = img[0]
        imageHeight = img[1]
        imageArray = img[6]

        # Create a PIL Image from our pixel array.
        imx = Image.frombytes("RGB", (imageWidth, imageHeight), imageArray)

        # Convert the PIL Image to a base64 encoded string
        buffered = io.BytesIO()
        imx.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return encoded_img
    
    def saveCameraImage(self, filepath):
        imx = self.getCameraImage()
        if imx == None:
            self._log_error("Cannot save the image from the startVideoFrameGrabberEvent!")
            return None
        imx.save(filepath, "PNG")
        return imx

    def sendCameraImage(self, ip, port):
        imx = self.getCameraImage()
        if imx == None: return None

        # Convert to grayscale
        img = imx.convert('L')
        aimg = img.tobytes()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))

            msg = '%9d\n' %len(aimg)
            s.send(msg.encode())
            s.send(aimg)

            data = s.recv(80)
            rcv_msg = data.decode()
            s.close()
            return rcv_msg
        except:
            self._log_error("Cannot send the image got from the startVideoFrameGrabberEvent!")
            return None
        
    
    
    

    
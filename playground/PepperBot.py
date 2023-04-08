import os, sys
import qi
from naoqi import ALProxy
import threading
import math
import time

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

        self.laserThread = None # TODO, or not


    def connect(self, ip="127.0.0.1", port=9559, alive = False):
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

        if self.services['ALBackgroundMovement'] != None:
            for aliveService in ['ALBackgroundMovement', 'ALBasicAwareness', 'ALSpeakingMovement']:
                if self.services[aliveService] != None:
                    self.services[aliveService].setEnabled(alive)
                    self._log_info("Alive service %s set to %s!" %(aliveService, str(alive)))
                else:
                    self._log_error("Alive service %s cannot be enabled/disabled." %(aliveService))

    def quit(self):
        self._log_info("Quitting robot...")
        self._init_robot()
        self._log_info("Quitted robot.")

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

    def waitForThread(self, thread_ref, service):
        if self.services[service] != None:
            self.services[service].wait(thread_ref, 0)
        else:
            self._log_error("Service %s not activated!" %(service))

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

    def startSensorThread(self):
        if self.sensorThread == None:
            self.sensorThread = threading.Thread(target=self._sensorThread, args=(self,))
            self.sensorThread.start()

    def stopSensorThread(self):
        if self.sensorThread != None:
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
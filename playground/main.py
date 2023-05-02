import os, sys
from pepperbot.PepperBot import PepperBot
import pepperbot.PepperMotions as motions

robot = PepperBot("127.0.0.1",45417,alive=False)

# robot.angleInterpolation(*bothArmsBumpInFront())
# robot.say("Hi Marco! My name is Pepper and this is a long sentence to see some basic functions!")

robot.stand()
ttt = robot.say("Hi Marco! My name is Pepper and this is a long sentence to see!", blocking=False)
# mt = robot.angleInterpolation(*bothArmsBumpInFront(), blocking=False)
# robot.waitForThread(mt, 'ALMotion')
robot.angleInterpolation(*motions.fancyRightArmCircle(), blocking=True)
# robot.angleInterpolation(*defaultPositionNeutral(), blocking=True)

# robot.angleInterpolation(*normalPosture())

# robot.eyesGreen(duration=1)
robot.stand()
robot.quit()
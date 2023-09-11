import os, sys, math

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

pepper_cmd.robot.say('Hello')
# pepper_cmd.robot.forward(0.5)
# pepper_cmd.robot.turn(360)
# pepper_cmd.robot.backward(0.5)
# pepper_cmd.robot.headPose(0, 0, 1) # use math.pi...
pepper_cmd.robot.dance()

end()
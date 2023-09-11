import qi
from pepperbot.PepperBotQi import PepperBot
import pepperbot.PepperMotions as motions

pbot = PepperBot("127.0.0.1",35775)

# pbot.setVolume(50) # working only when service is on!

sayThread = pbot.say("Ciao Marco! Sono PepperBot! Come va?", blocking=False)
pbot.angleInterpolation(*motions.fancyRightArmCircle(), blocking=True)

pbot.say("Altra azione perche' mi va di farla!", blocking=False)
pbot.angleInterpolation(*motions.bothArmsBumpInFront(), blocking=True)
pbot.eyesGreen(duration=1)

pbot.stand()

pbot.quit()
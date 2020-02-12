from Phidget22.Phidget import *
from Phidget22.Devices.Encoder import *
import time
import rospy

def onPositionChange(self, positionChange, timeChange, indexTriggered):
	print("PositionChange: " + str(positionChange))
	print("TimeChange: " + str(timeChange))
	print("IndexTriggered: " + str(indexTriggered))
	print("----------")

def main():
	encoder0 = Encoder()

	encoder0.getPosition(onPositionChange)

	encoder0.openWaitForAttachment(5000)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	encoder0.close()

main()
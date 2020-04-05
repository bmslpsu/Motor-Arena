#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from Phidget22.Devices.Encoder import *
# from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, AInFlag)
#
# import rospy
#
# from std_msgs.msg import Header
# from mcdaq.msg import MC_AnalogIN
#
# from dynamic_reconfigure.server import Server
# from mcdaq.cfg import mcdaqConfig

class EncoderRead:

	def __init__(self):
		self.countprev = 324
		self.inputA = 0
		
		self.encoder0 = Encoder()
		self.encoder0.setOnPositionChangeHandler(self.onPositionChange)
		self.encoder0.openWaitForAttachment(5000)
		self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())
	
	def onPositionChange(self, test1,test2,test3,test4):
		self.totcount = self.encoder0.getPosition()
		print(self.totcount)
		# print("PositionChange: " + str(globalposition))
		# print("TimeChange: " + str(timeChange))
		# print("----------")

	# def run(self):
	
	
if __name__ == '__main__':
	main = EncoderRead()
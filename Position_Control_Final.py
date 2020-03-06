from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID                                  # PID library
import time
import pandas                                               # Reading and Writing .csv file
import matplotlib.pyplot as plt                             # Ploting trajectory
import numpy

class Position_Control:
    def __init__(self):
        self.cpr = 324                                      # Number of count per Revolution of Encoder
        self.iniVelocity = 1                              # initial velocity
        self.samplingrate = 0.001                           # samplingrate of trajectory (second)
        self.pid = PID(0.002, 0, 0.002, setpoint=0)           # PID control gain
#=======================================================================================================================
        self.ii = 0
        self.totcount = 0                                   # Position Counter
        self.numEncoderRead = 0                             # Number of time gathering data from encoder
        self.timemult = (1/self.samplingrate)*100           # millisecond
        self.timeval0 = int(time.time() * self.timemult)    # initialize the starting time, t0

    def setup(self):
        self.encoder0 = Encoder()                           # setup encoder and motor from Phidget Library
        self.dcMotor0 = DCMotor()

        self.degToCount()  # Load in desired position       # loading the .csv desired trajectory
        self.motorposition = [0]*(len(self.targetCount))    # Initialize the array to record data into .csv
        self.motortime = [0] * (len(self.targetCount))
        self.diffhist = [0] * (len(self.targetCount))       # Difference bwtween desired and actual motor position

        self.encoder0.openWaitForAttachment(5000)           # Open Phidget Channel and wait for 5 second for data
        self.dcMotor0.openWaitForAttachment(5000)

        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())   # Set the encoder reading interval to minimum, which is 8 ms
        self.dcMotor0.setTargetVelocity(self.iniVelocity)                   # set motor to inivial speed.
        self.encoder0.setOnPositionChangeHandler(self.encoderread)          # Like a Interrupt function, call encoderread function to position

        while self.ii != len(self.targetCount):             # Loop through the value in target trajectory
            self.positionControl()                          # main function to control the motor position
            self.getdata()                                  # Record the time and position data, will be converted into .csv file.
            self.ii = self.ii + 1

        self.encoder0.close()                               # Turn off encoder and motor
        self.dcMotor0.close()

        self.writecsv()                                     # Write the Data in getdata function into a .csv file
        self.ploting()                                      # Plot the scatter plot of desired and actual motor position

    def positionControl(self):
        target = self.targetCount[self.ii]                  # getting one value from the target trajectory array
        while (self.gettime() % 100) != 0:                  # Time Pulling, control the motor position every 0.001 second
            pass
        self.diffhist[self.ii] = self.totcount- target      # compute the difference between Desired and Actual Position

        velocity = self.PIDposition(self.diffhist[self.ii]) # Using PID to compute the required velocity
        self.dcMotor0.setTargetVelocity(velocity)           # set velocity between -1 to 1 to Phidget Motor driver

    def PIDposition(self,currentloca):
        velocity = self.pid(currentloca)                    # use PID library to compute velovity
        if 1 < velocity:                                    # Bound the velocity between -1 and 1
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        self.totcount = self.encoder0.getPosition()         # Read encoder count when the encoder is turning
        self.numEncoderRead = self.numEncoderRead + 1       # Number of time encoder recording data

    def getdata(self):
        self.motortime[self.ii] = self.gettime()            # compute the time spent since the t0
        self.motorposition[self.ii] = self.totcount         # record the motor position for .csv file

    def degToCount(self):
        angle = self.readcsv()                              # read the target angle from .csv file
        self.targetCount = [0] * len(angle)                 # create a same size array as target angle
        for ii in range(0, len(angle)):
            self.targetCount[ii] = int(angle[ii] * self.cpr / 360)  # convert angle into the count according to the cpr of the encoder

    def gettime(self):
        timeval1 = int(time.time() * self.timemult)
        self.timedif = float(timeval1 - self.timeval0)
        return self.timedif

    def readcsv(self):
        reader = pandas.read_csv("/home/george/Desktop/Testing_Figure/Trajectory/1Hz_Since_360deg.csv", sep=',')    # read target angle as .csv file
        return reader.Angle

    def writecsv(self):
        table = [0]*(len(self.motortime)+1)                 # Create a table to store time spend, motor position history and difference between target and actual position
        table[0] = ["Time",'\t',"Position",'\t',"Error"]    # the heading for each column
        for ii in range(1,len(table)):                      # Import information into each cell of table array
            time = self.motortime[ii-1]-self.motortime[1]
            table[ii] = [time,'\t',self.motorposition[ii-1],'\t',self.diffhist[ii-1]]
        df = pandas.DataFrame(table)                        # convert table array into pandas dataFrame
        df.to_csv("CSVWriting.csv", index=False, header=False) # write into .csv file named CSVWriting.csv


    def ploting(self):
        x = numpy.linspace(0, 10, 10000)                    # ploting the comparison between Desired trajectory and actual motor trajectory
        tt = [0.1]*len(self.motortime)
        t0 = self.motortime[1]
        for ii in range (len(self.motortime)):
            tt[ii] = (self.motortime[ii]-self.motortime[1])/self.timemult

        plt.scatter(x, self.targetCount, c='b', s=10)
        plt.scatter(tt, self.motorposition, c='y', s=10)
        plt.title('1Hz_Since_360deg')
        plt.legend(['Target','Actual'])
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.show()

if __name__ == '__main__':
    main = Position_Control()
    main.setup()
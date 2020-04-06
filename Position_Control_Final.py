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
        self.cpr = 324                                          # Number of count per Revolution of Encoder
        self.iniVelocity = 0.25                                 # initial velocity
        self.samplingrate = 0.001                               # samplingrate of trajectory (second)
        self.pid = PID(0.015, 0.00001 , 0.0002, setpoint=0)     # PID control gain
        self.trajectoryRoot = "sampleTrajectory/PositionControl/0.5Hz_Sine_40deg.csv" # Desired Trajectory Root
        self.motorHistoryRoot = "CSVWriting.csv"                # History Storing Root
#=======================================================================================================================
        self.ii = 0
        self.encoderCount = 0                                   # Position Counter
        self.timeMult = (1/self.samplingrate)*100               # Converting time.time unit to millisecond
        self.encoderTime = 0                                    # initialized the encoder time reading variable

    def setup(self):
        self.encoder0 = Encoder()                               # setup encoder and motor from Phidget Library
        self.dcMotor0 = DCMotor()
        self.degToCount()                                       # loading the .csv desired trajectory, convert Angle into Count of the Encoder

        # Define the variables to store trajectory history, will be writen into .csv file
        self.motorPosition = [0]*(len(self.targetCount))        # Position History
        self.motorTime = [0] * (len(self.targetCount))          # Time History
        self.motorPositionDiff = [0] * (len(self.targetCount))  # Difference between desired and actual motor position
        self.analogOut = [0] * (len(self.targetCount))          # analog output History

        self.encoder0.openWaitForAttachment(5000)           # Open Phidget Channel and wait for 5 second for data
        self.dcMotor0.openWaitForAttachment(5000)

        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())   # Set the encoder reading interval to minimum, which is 8 ms for Phidget 1065_1 Motor Driver
        self.dcMotor0.setTargetVelocity(self.iniVelocity)                   # set motor to inivial speed.
        self.encoder0.setOnPositionChangeHandler(self.encoderread)          # Like a Interrupt function, call encoderread function to position

        self.time0 = time.time() * self.timeMult  # initialize the starting time, Time 0

        while self.ii != len(self.targetCount):             # Loop through the value in target trajectory
            self.positionControl()                          # main function to control the motor position
            self.getdata()                                  # Record the time and position data, will be converted into .csv file.
            self.ii = self.ii + 1                           # increment variable

        self.encoder0.close()                               # Turn off encoder and motor
        self.dcMotor0.close()

        self.writecsv()                                     # Write the Data in getdata function into a .csv file
        self.ploting()                                     # Plot the scatter plot of desired and actual motor position

    def positionControl(self):
        target = self.targetCount[self.ii]                  # getting one value from the target trajectory array
        while (self.pullingtime() % 100) != 0:              # Time Pulling, control the motor position every 0.001 second
            pass
        self.motorPositionDiff[self.ii] = self.encoderCount- target     # compute the difference between Desired and Actual Position
        velocity = self.PIDposition(self.motorPositionDiff[self.ii])    # Using PID to compute the required velocity
        self.dcMotor0.setTargetVelocity(velocity)                       # set velocity between -1 to 1 to Phidget Motor driver

    def PIDposition(self,currentloca):
        velocity = self.pid(currentloca)                    # use PID library to compute velovity
        self.analogOut[self.ii] = velocity
        if 1 < velocity:                                    # Bound the velocity between -1 and 1
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        self.encoderCount = self.encoder0.getPosition()         # Read encoder count when the encoder is turning
        self.encoderTime = time.time()*self.timeMult            # Read the time when turning detected

    def getdata(self):
        self.motorTime[self.ii] = (self.encoderTime - self.time0)/self.timeMult         # compute the time spent since the t0
        if self.motorTime[self.ii] < 0:                                                 # Ensure Positive time value
            self.motorTime[self.ii] = 0
        self.motorPosition[self.ii] = self.encoderCount                                 # record the motor position for .csv file

    def degToCount(self):
        angle = self.readcsv()                              # read the target angle from .csv file
        self.targetCount = [0] * len(angle)                 # create a same size array as target angle
        for ii in range(0, len(angle)):
            self.targetCount[ii] = int(angle[ii] * self.cpr / 360)  # convert angle into the count according to the cpr of the encoder

    def pullingtime(self):                                  # Time Pulling function for accurate sampling time
        timepulling = time.time() * self.timeMult
        timepass = int((timepulling - self.time0))
        return timepass

    def readcsv(self):
        reader = pandas.read_csv(self.trajectoryRoot, sep=',')    # read target Trajectory from a .csv file
        return reader.Angle

    def writecsv(self):
        table = [0]*(len(self.motorTime)+1)                                     # Create a table to store time spend, motor position history and difference between target and actual position
        table[0] = ["Time",'\t',"Position",'\t',"AnalogVolt",'\t',"Error"]      # the heading for each column
        for ii in range(1,len(table)):                                          # Import information into each cell of table array
            table[ii] = [self.motorTime[ii-1],'\t',self.motorPosition[ii-1],'\t',self.analogOut[ii-1],'\t',self.motorPositionDiff[ii-1]]
        df = pandas.DataFrame(table)                                            # convert table array into pandas dataFrame
        df.to_csv(self.motorHistoryRoot, index=False, header=False)             # write into .csv file named CSVWriting.csv


    def ploting(self):
        x = numpy.linspace(0, 10, 10000)                    # ploting the comparison between Desired trajectory and actual motor trajectory

        plt.plot(x, self.targetCount,'b-')
        plt.plot(self.motorTime, self.motorPosition,'y-')
        plt.title('0.1Hz_Sine_40deg', fontsize=25)
        plt.legend(['Target', 'Actual'], fontsize=25,loc = 'upper right')
        plt.xlabel('Time')
        plt.ylabel('Count')

        plt2 = plt.twinx()
        plt2.set_ylabel('Voltage Output(V)', color='red')
        plt2.tick_params(axis='y', labelcolor='red')
        plt2.plot(self.motorTime, self.analogOut, 'r-')
        plt.show()

if __name__ == '__main__':
    main = Position_Control()
    main.setup()
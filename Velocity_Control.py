from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID                                  # PID library
import time
import pandas                                               # Reading and Writing .csv file
import matplotlib.pyplot as plt                             # Ploting trajectory
import numpy

class Velocity_Control:
    def __init__(self):
        self.cpr = 324.0                                      # Number of count per Revolution of Encoder
        self.iniVelocity = 0.25                               # initial velocity
        self.samplingrate = 0.001                           # samplingrate of trajectory (second)
        self.pid = PID(0.01 , 0 , 0, setpoint=0)           # PID control gain
        self.numstored = 25
#=======================================================================================================================
        self.ii = 0
        self.numEncoderRead = 0                             # Number of time gathering data from encoder
        self.RPMDiff = 0
        self.timeMult = (1/self.samplingrate)*100           # millisecond
        self.encoderCount = [0]*self.numstored
        self.encoderTime = [0] *self.numstored

    def setup(self):
        self.encoder0 = Encoder()                           # setup encoder and motor from Phidget Library
        self.dcMotor0 = DCMotor()
        self.readcsv()

        self.motorTime = [0] * (len(self.targetVelocity))
        self.motorRPM = [0] * (len(self.targetVelocity))
        self.motorPosition = [0]*(len(self.targetVelocity))    # Initialize the array to record data into .csv
        self.motorRPMDiff = [0] * (len(self.targetVelocity))       # Difference bwtween desired and actual motor position
        self.motorAnalogOut = [0] * (len(self.targetVelocity))

        self.encoder0.openWaitForAttachment(5000)           # Open Phidget Channel and wait for 5 second for data
        self.dcMotor0.openWaitForAttachment(5000)

        self.dcMotor0.setTargetVelocity(self.iniVelocity)                   # set motor to inivial speed.
        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())   # Set the encoder reading interval to minimum, which is 8 ms
        self.encoder0.setOnPositionChangeHandler(self.encoderread)  # Like a Interrupt function, call encoderread function to position

        self.time0 = time.time() * self.timeMult
        self.encoderTime = [self.time0]* self.numstored


        while self.ii != len(self.targetVelocity):             # Loop through the value in target trajectory
            self.velocityControl()                          # main function to control the motor position
            self.getdata()                                  # Record the time and position data, will be converted into .csv file.
            self.ii = self.ii + 1

        self.encoder0.close()                               # Turn off encoder and motor
        self.dcMotor0.close()

        self.writecsv()                                     # Write the Data in getdata function into a .csv file
        #self.ploting()                                      # Plot the scatter plot of desired and actual motor position

    def velocityControl(self):
        target = self.targetVelocity[self.ii]                  # getting one value from the target trajectory array
        while (self.pullingtime() % 100) != 0:                  # Time Pulling, control the motor position every 0.001 second
            pass
        self.getRPM()
        self.RPMDiff = self.currentRPM - target      # compute the difference between Desired and Actual Position
        velocity = self.PIDvelocity(self.RPMDiff) # Using PID to compute the required velocity
        #velocity = 0.25
        self.dcMotor0.setTargetVelocity(velocity)           # set velocity between -1 to 1 to Phidget Motor driver

    def PIDvelocity(self,RPMDiff):
        velocity = self.pid(RPMDiff)                    # use PID library to compute velovity
        self.motorAnalogOut[self.ii] = velocity
        if 1 < velocity:                                    # Bound the velocity between -1 and 1
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        for ii in range (self.numstored-1):
            self.encoderCount[ii] =self.encoderCount[ii+1]
            self.encoderTime[ii] = self.encoderTime[ii + 1]

        self.encoderCount[self.numstored-1] = self.encoder0.getPosition()         # Read encoder count when the encoder is turning
        self.encoderTime[self.numstored-1] = time.time()*self.timeMult

        self.numEncoderRead = self.numEncoderRead + 1       # Number of time encoder recording data

    def pullingtime(self):
        timepulling = time.time()*self.timeMult
        self.timepass = int((timepulling - self.time0))
        return self.timepass

    def getRPM(self):
        countDiff = (self.encoderCount[self.numstored-1]-self.encoderCount[0])
        timeDiff = (self.encoderTime[self.numstored-1]-self.encoderTime[0])
        if timeDiff == 0:
            timeDiff=1
        self.currentRPM = ((countDiff/self.cpr)/(timeDiff)*self.timeMult)*60

    def getdata(self):
        self.motorTime[self.ii] = (self.encoderTime[self.numstored-1] - self.time0)/self.timeMult         # compute the time spent since the t0
        self.motorPosition[self.ii] = self.encoderCount[self.numstored-1]         # record the motor position for .csv file
        self.motorRPM[self.ii] = self.currentRPM
        self.motorRPMDiff[self.ii] = -self.RPMDiff

    def readcsv(self):
        reader = pandas.read_csv("0.1Hz_Since_250rpm.csv", sep=',')    # read target angle as .csv file
        self.targetVelocity = reader.Velocity

    def writecsv(self):
        table = [0]*(len(self.motorTime)+1)                 # Create a table to store time spend, motor position history and difference between target and actual position
        table[0] = ["Time",'\t',"RPM",'\t',"Position",'\t',"RPMDifferent",'\t',"AnalogOutput"]    # the heading for each column
        for ii in range(1,len(table)):                      # Import information into each cell of table array
            time = self.motorTime[ii-1]-self.motorTime[1]
            table[ii] = [time,'\t',self.motorRPM[ii-1],'\t',self.motorPosition[ii-1],'\t',self.motorRPMDiff[ii-1],'\t',self.motorRPMDiff[ii-1],'\t',self.motorAnalogOut[ii-1]]
        df = pandas.DataFrame(table)                        # convert table array into pandas dataFrame
        df.to_csv("CSVWriting.csv", index=False, header=False) # write into .csv file named CSVWriting.csv


    def ploting(self):
        x = numpy.linspace(0, 10, 10000)                    # ploting the comparison between Desired trajectory and actual motor trajectory
        tt = [0.1]*len(self.motorTime)
        t0 = self.motorTime[1]
        for ii in range (len(self.motorTime)):
            tt[ii] = (self.motorTime[ii]-self.motorTime[1])/self.timeMult

        plt.plot(x, self.targetCount,'b-')
        plt.plot(tt, self.motorposition,'y-')
        plt.title('0.1Hz_Sine_40deg', fontsize=25)
        plt.legend(['Target', 'Actual'], fontsize=25,loc = 'upper right')
        plt.xlabel('Time')
        plt.ylabel('Count')

        plt2 = plt.twinx()
        plt2.set_ylabel('Voltage Output(V)', color='red')
        plt2.tick_params(axis='y', labelcolor='red')
        plt2.plot(tt, self.velocity, 'r-')
        plt.show()

if __name__ == '__main__':
    main = Velocity_Control()
    main.setup()
import pandas
import matplotlib.pyplot as plt
import numpy

class Ploting:
    def __init__(self):
        self.filetrajecory = "trajectory.csv"
        self.filemotorhist = "CSVWriting.csv"
        self.cpr = 324
        self.timemult = 100000

    def readfile(self):
        readertra = pandas.read_csv("/home/george/Desktop/Testing_Figure/Trajectory/NewTraj/0.5Hz_Sine_40deg.csv", sep=',')
        readerhist = pandas.read_csv("CSVWriting.csv", sep=',')
        self.trajectory = [0]*len(readertra)
        for ii in range(0, len(readertra)):
            self.trajectory[ii] = int(readertra.Angle[ii] * self.cpr / 360)

        self.motortime = readerhist.Time
        self.motorposition = readerhist.Position
        self.velocity = readerhist.AnalogVolt
        self.diff = readerhist.Error

    def plot(self):
        x = numpy.linspace(0, 10, 10000)
        tt = [0.1] * len(self.motortime)
        for ii in range (len(self.motortime)):
            tt[ii] = (self.motortime[ii])/self.timemult

        plt.plot(x, self.trajectory,'b-')
        plt.plot(tt, self.motorposition,'y-')
        plt.title('0.5Hz_Sine_40deg', fontsize=25)
        plt.legend(['Target','Actual'], fontsize=25,loc = 'upper right')
        plt.xlabel('Time')
        plt.ylabel('Count')

        plt2 = plt.twinx()
        plt2.set_ylabel('Voltage Output(V)', color = 'red')
        plt2.tick_params(axis='y', labelcolor='red')
        plt2.plot(tt,self.velocity,'r-')
        plt.show()

if __name__ == '__main__':
    main = Ploting()
    main.readfile()
    main.plot()
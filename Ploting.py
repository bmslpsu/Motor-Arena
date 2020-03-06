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
        readertra = pandas.read_csv("/home/george/Desktop/Testing_Figure/Trajectory/0.5Hz_Since_360deg.csv", sep=',')
        readerhist = pandas.read_csv("CSVWriting.csv", sep=',')
        self.trajectory = [0]*len(readertra)
        for ii in range(0, len(readertra)):
            self.trajectory[ii] = int(readertra.Angle[ii] * self.cpr / 360)

        self.motortime = readerhist.Time
        self.motorposition = readerhist.Position

    def plot(self):
        x = numpy.linspace(0, 10, 10000)
        tt = [0.1] * len(self.motortime)
        for ii in range (len(self.motortime)):
            tt[ii] = (self.motortime[ii])/self.timemult

        plt.scatter(x, self.trajectory, c = 'b',s = 10)
        plt.scatter(tt, self.motorposition,c = 'y',s = 10)
        plt.title('0.5Hz_Since_360deg')
        plt.legend(['Target','Actual'])
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.show()

if __name__ == '__main__':
    main = Ploting()
    main.readfile()
    main.plot()
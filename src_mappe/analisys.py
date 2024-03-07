import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import re
import sys
import datetime


class GpxReadout:
    coordinate = []
    times = []
    hr = []
    ele = []
    numpoints = 0
    numhr = 0
    numtime = 0
    numele = 0


    def __init__(self, filepath: str):
    # readout of the gpx file
        with open(filepath, "r") as file:
            intopoints = False
            for line in file:
                if not intopoints:
                    if re.match("\s*<trk>\s*", line) is not None:
                        intopoints = True
                else:
                    testpoint = re.match("\s*<trkpt\slat=\"([0-9]{2}.[0-9]*)\"\slon=\"([0-9]{2}.[0-9]*)\">\s*",
                                         line)
                    if testpoint is not None:
                        self.numpoints += 1
                        self.coordinate.append([float(testpoint.group(1)), float(testpoint.group(2))])
                        if self.numpoints % 1000 == 0:
                            sys.stdout.write(str(self.numpoints) + "\r")
                            sys.stdout.flush()
                    else:
                        testtime = re.match("\s*<time>[0-9]{4}-[0-9]{2}-[0-9]{2}T([0-9]{2}\:[0-9]{2}:[0-9]{2})\.000Z</time>\s*",
                                            line)
                        if testtime is not None:
                            self.numtime += 1
                            if self.numtime != self.numpoints:
                                for i in range(self.numpoints - self.numtime):
                                    self.times.append(datetime.time.fromisoformat('00:00:00'))
                                self.numtime = self.numpoints
                            else:
                                pass
                            time_obj = datetime.time.fromisoformat(testtime.group(1))
                            self.times.append(time_obj)
                        else:
                            testhr = re.match("\s*<ns3:hr>([0-9]+)</ns3:hr>\s*", line)
                            if testhr is not None:
                                self.numhr += 1
                                if self.numhr != self.numpoints:
                                    for i in range(self.numpoints - self.numhr):
                                        self.hr.append(np.nan)
                                    self.numhr = self.numpoints
                                else:
                                    pass
                                self.hr.append(int(testhr.group(1)))
                            else:
                                testele = re.match("\s*<ele>([0-9]+)\.[0-9]+</ele>\s*", line)
                                if testele is not None:
                                    self.numele += 1
                                    if self.numele != self.numpoints:
                                        for i in range(self.numpoints - self.numele):
                                            self.ele.append(None)
                                        self.numele = self.numpoints
                                    else:
                                        pass
                                    self.ele.append(int(testele.group(1)))
                                else:
                                    pass

        self.coordinate = np.array(self.coordinate)
        self.coordinate[:, 0] = self.coordinate[:, 0] / np.max(self.coordinate[:, 0])
        self.coordinate[:, 1] = self.coordinate[:, 1] / np.max(self.coordinate[:, 1])
        self.times = np.array(self.times)

        def tosec(x):
                return (x.hour * 60 + x.minute) * 60 + x.second

        tosec_vec = np.vectorize(tosec)

        self.elap_time = tosec_vec(self.times) - tosec(min(self.times))
        self.hr = np.array(self.hr)
        self.ele = np.array(self.ele)

    
    def convert_elap(self, timesec):
        eth = np.floor(timesec / 3600).astype(int)
        etm = np.floor((timesec - 3600 * eth) / 60).astype(int)
        ets = (timesec - 3600 * eth - 60 * etm).astype(int)
        return str(eth) + ":" + str(etm) + ":" + str(ets)

    


def plottrack(gpx: GpxReadout, timeinput: np.ndarray, outpath: str):
    fig, ax = plt.subplots()
    if gpx.numele != 0:
        plot = ax.scatter(gpx.coordinate[:, 1], gpx.coordinate[:, 0], s=5, c=gpx.ele, cmap='viridis_r')
        handles, labels = plot.legend_elements(prop="colors", alpha = 0.6)
        ax.legend(handles, labels, loc = "lower left", title = "altitudine")
    else:
        ax.scatter(gpx.coordinate[:, 1], gpx.coordinate[:, 0], s=5)

    ax.tick_params(
        axis = "both",
        which = "both",
        bottom = False,
        left = False,
        labelbottom = False,
        labelleft = False
    )
    startpoint = np.reshape(gpx.coordinate[gpx.times == min(gpx.times)], 2)
    endpoint = np.reshape(gpx.coordinate[gpx.times == max(gpx.times)], 2)
    ax.scatter(startpoint[1], startpoint[0], s=60, color='green')
    ax.scatter(endpoint[1], endpoint[0], s=60, color='red')

    timeinput = np.array([datetime.time.fromisoformat(x) for x in timeinput])

    count_images = 0

    for ts in timeinput:
        ubtime = datetime.time(hour=ts.hour, minute=ts.minute, second=59)
        lbtime = datetime.time(hour=ts.hour, minute=ts.minute, second=0)
        coord_time = gpx.coordinate[np.logical_and(gpx.times > lbtime, gpx.times < ubtime)]
        pointpos = np.average(coord_time[:, 0:2], axis=0)

        count_images += 1
        ax.annotate(str(count_images), xy=(pointpos[1], pointpos[0]), xytext=(30, 30),
                    textcoords='offset points',
                    color='k', size='large',
                    arrowprops=dict(
                    arrowstyle='simple,tail_width=0.2,head_width=0.8,head_length=0.8',
                    color='k'))
    fig.savefig(outpath + 'track.pdf', bbox_inches = "tight")
    plt.close(fig)
    return count_images


def plothr(gpx: GpxReadout, outpath: str):
    if gpx.numhr != 0:
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: gpx.convert_elap(x)))
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlabel('Time [H:M:S]')
        ax.set_ylabel('Heart rate [BPM]')
        ax.grid()
        ax.plot(gpx.elap_time, gpx.hr, color='red')
        fig.savefig(outpath + 'hr.pdf')
        plt.close(fig)
        return 0
    else:
        return -1


def plotele(gpx: GpxReadout, outpath: str):
    if gpx.numele != 0:
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: gpx.convert_elap(x)))
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_xlabel('Time [H:M:S]')
        ax.set_ylabel('Elevation [m SLM]')
        ax.grid()
        ax.plot(gpx.elap_time, gpx.ele, color='green')
        fig.savefig(outpath + 'ele.pdf')
        plt.close(fig)
        return 0
    else:
        return -1


def main():
    path = ''
    outpath = ''
    timestrings = []

    # arguments parsing bruttissimo 

    for argind in range(len(sys.argv)):
        if sys.argv[argind] == "-p":
            argind += 1
            path = sys.argv[argind]
        if sys.argv[argind] == "-op":
            argind += 1
            outpath = sys.argv[argind]
        if sys.argv[argind] == "-t":
            timestrings = []
            argind += 1
            while re.match("-[a-z]", sys.argv[argind]) is None:
                timestrings.append(sys.argv[argind])
                if(argind == len(sys.argv) - 1):
                    break
                else:
                    argind += 1

    gpx = GpxReadout(path)
    plottrack(gpx, timestrings, outpath)
    plothr(gpx, outpath)
    plotele(gpx, outpath)


if __name__ == "__main__":
    main()

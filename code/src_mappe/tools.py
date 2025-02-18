import numpy as np
import re
import datetime
import sys


class GpxReadout:
    def __init__(self, filepath: str):
        self.coordinate_raw = []
        self.coordinate = []
        self.times = []
        self.days = []
        self.hr = []
        self.ele = []
        self.numpoints = 0
        self.numhr = 0
        self.numtime = 0
        self.numele = 0
        self.ismultiday = True
        # readout of the gpx file
        with open(filepath, "r") as file:

            intopoints = False
            for line in file:
                if not intopoints:
                    if re.match(r"\s*<trk>\s*", line) is not None:
                        intopoints = True
                else:
                    testpoint = re.match(r"\s*<trkpt\slat=\"([0-9]{2}.[0-9]*)\"\slon=\"([0-9]{2}.[0-9]*)\">\s*",
                                         line)
                    if testpoint is not None:
                        self.numpoints += 1
                        self.coordinate.append([float(testpoint.group(1)), float(testpoint.group(2))])
                        if self.numpoints % 1000 == 0:
                            sys.stdout.write(str(self.numpoints) + "\r")
                            sys.stdout.flush()
                        continue

                    testtime = re.match(r"\s*<time>([0-9]{4}-[0-9]{2}-[0-9]{2})T([0-9]{2}\:[0-9]{2}:[0-9]{2})\.000Z</time>\s*",
                                        line)
                    if testtime is not None:
                        self.numtime += 1
                        if self.numtime != self.numpoints:
                            for i in range(self.numpoints - self.numtime):
                                self.times.append(datetime.time.fromisoformat('00:00:00'))
                                self.days.append(datetime.datetime.fromisoformat('1970-01-01'))
                            self.numtime = self.numpoints
                        time_obj = datetime.time.fromisoformat(testtime.group(2))
                        day_obj = datetime.datetime.fromisoformat(testtime.group(1))
                        self.times.append(time_obj)
                        self.days.append(day_obj)
                        continue

                    testhr = re.match(r"\s*<ns3:hr>([0-9]+)</ns3:hr>\s*",
                                      line)
                    if testhr is not None:
                        self.numhr += 1
                        if self.numhr != self.numpoints:
                            for i in range(self.numpoints - self.numhr):
                                self.hr.append(np.nan)
                            self.numhr = self.numpoints
                        self.hr.append(int(testhr.group(1)))
                        continue

                    testele = re.match(r"\s*<ele>([0-9]+)(\.[0-9]+)?</ele>\s*", line)
                    if testele is not None:
                        self.numele += 1
                        if self.numele != self.numpoints:
                            for i in range(self.numpoints - self.numele):
                                self.ele.append(None)
                            self.numele = self.numpoints
                        self.ele.append(int(testele.group(1)))

            # check if the number of points is consistent for the last cycles
            if self.numtime != self.numpoints:
                for i in range(self.numpoints - self.numtime):
                    self.times.append(datetime.time.fromisoformat('00:00:00'))
                    self.days.append(datetime.datetime.fromisoformat('1970-01-01'))
                    self.numtime = self.numpoints
            if self.numhr == 0:
                pass
            elif self.numhr != self.numpoints:
                for i in range(self.numpoints - self.numhr):
                    self.hr.append(np.nan)
                    self.numhr = self.numpoints
            if self.numele == 0:
                pass
            elif self.numele != self.numpoints:
                for i in range(self.numpoints - self.numele):
                    self.ele.append(None)
                    self.numele = self.numpoints

        self.coordinate = np.array(self.coordinate)
        self.times = np.array(self.times)
        self.days = np.array(self.days)
        if np.all(self.days == self.days[0]):
            # if the day is always the same is enough to keep one daytime obj
            self.days = self.days[0]
            self.ismultiday = False

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

    def get_extremes(self):
        startcoords = [self.coordinate[self.times == min(self.times), 0],
                           self.coordinate[self.times == min(self.times), 1]]
        endcoords = [self.coordinate[self.times == max(self.times), 0],
                         self.coordinate[self.times == max(self.times), 1]]
        extele = [self.ele[self.times == min(self.times)],
                  self.ele[self.times == max(self.times)]]
        exttimes = [min(self.times), max(self.times)]
        if self.ismultiday:
            extdays = [min(self.days), max(self.days)]
        else:
            extdays = [self.days, self.days]
        return {'startcoords': startcoords,
                'endcoords': endcoords,
                'extele': extele,
                'exttimes': exttimes,
                'extdays': extdays}
    
    def normalized_coords(self):
        coordinate_norm = np.zeros(np.shape(self.coordinate))
        coordinate_norm[:, 0] = self.coordinate[:, 0] / np.max(self.coordinate[:, 0])
        coordinate_norm[:, 1] = self.coordinate[:, 1] / np.max(self.coordinate[:, 1])

        startcoords_norm = [self.coordinate_norm[self.times == min(self.times), 0],
                       self.coordinate_norm[self.times == min(self.times), 1]]
        endcoords_norm = [self.coordinate_norm[self.times == max(self.times), 0],
                     self.coordinate_norm[self.times == max(self.times), 1]]
        
        return {'coordinate_norm': coordinate_norm,
                'startcoords_norm': startcoords_norm,
                'endcoords_norm': endcoords_norm}


def parse_args(arglist):
    args = {}
    key = ''
    arglist = arglist[1:]
    for i in arglist:
        rexp = re.match('-([a-z]+)', i)
        if rexp:
            key = rexp.group(1)
            args[key] = []
        else:
            if key == '':
                print('errore nel parsing')
                return -1
            args[key].append(i)
    return args

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import sys
import datetime
import tools as tl


def plottrack(gpx: tl.GpxReadout, outpath: str, timeinput: np.ndarray = None):
    fig, ax = plt.subplots()
    if gpx.numele != 0:
        plot = ax.scatter(gpx.coordinate[:, 1], gpx.coordinate[:, 0], s=5, c=gpx.ele, cmap='viridis_r')
        handles, labels = plot.legend_elements(prop="colors", alpha=0.6)
        ax.legend(handles, labels, loc="lower left", title="altitudine")
    else:
        ax.scatter(gpx.coordinate[:, 1], gpx.coordinate[:, 0], s=5)

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False
    )
    startpoint = np.reshape(gpx.coordinate[gpx.times == min(gpx.times)], 2)
    endpoint = np.reshape(gpx.coordinate[gpx.times == max(gpx.times)], 2)
    ax.scatter(startpoint[1], startpoint[0], s=60, color='green')
    ax.scatter(endpoint[1], endpoint[0], s=60, color='red')
    

    count_images = 0
    if timeinput is not None:
        timeinput = np.array([datetime.time.fromisoformat(x) for x in timeinput])

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
    fig.savefig(outpath + 'track.pdf', bbox_inches="tight")
    plt.close(fig)
    return count_images


def plotmultiday(gpxs: list, outpath: str):
    tracks = []
    tracks_ele = []
    tracks_extremes = []
    trek_days = []
    for gpx in gpxs:
        if isinstance(gpx.days, np.ndarray):
            trek_days.append(min(gpx.days))
        else:
            trek_days.append(gpx.days)
        tracks.append(gpx.coordinate_raw)
        tracks_ele.append(gpx.ele)
        tracks_extremes.append([[gpx.coordinate_raw[gpx.times == min(gpx.times), 0],
                                 gpx.coordinate_raw[gpx.times == min(gpx.times), 1]],
                                [gpx.coordinate_raw[gpx.times == max(gpx.times), 0],
                                 gpx.coordinate_raw[gpx.times == max(gpx.times), 1]]])

    tracks_extremes = np.array(tracks_extremes)
    trek_days = np.array(trek_days)

    maxx = max([max(t[:, 0]) for t in tracks])
    maxy = max([max(t[:, 1]) for t in tracks])

    for t in tracks:
        t[:, 0] = t[:, 0] / maxx
        t[:, 1] = t[:, 1] / maxy

    tracks_extremes[:, :, 0] = tracks_extremes[:, :, 0] / maxx
    tracks_extremes[:, :, 1] = tracks_extremes[:, :, 1] / maxy

    fig, ax = plt.subplots()
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False
    )

    counter = 0
    colmaps = ['viridis_r', 'plasma_r', 'inferno_r', 'magma_r', 'cividis_r']
    for t, e in zip(tracks, tracks_ele):
        ax.scatter(t[:, 1], t[:, 0], s=5, c=e, cmap=colmaps[counter % len(colmaps)])
        counter += 1

    counter = 0
    for e in tracks_extremes:
        ax.scatter(e[0, 1], e[0, 0], s=60, c='k') # start of the day
        ax.scatter(e[1, 1], e[1, 0], s=60, c='k') # end of the day
        # adding "notte numero " annotation
        if counter != np.shape(tracks_extremes)[0]-1:    
            ax.annotate("Notte " + str(counter + 1), xy=(e[1, 1], e[1, 0]), xytext=(30, 30),
                        textcoords='offset points',
                        color='k', size='large',
                        arrowprops=dict(
                        arrowstyle='simple,tail_width=0.2,head_width=0.8,head_length=0.8',
                        color='k'))
        counter += 1

    ax.scatter(tracks_extremes[trek_days == max(trek_days), 1, 1], # end of the last day
               tracks_extremes[trek_days == max(trek_days), 1, 0],
               s=90, c='r')
    ax.scatter(tracks_extremes[trek_days == min(trek_days), 0, 1], # start of the first day
               tracks_extremes[trek_days == min(trek_days), 0, 0],
               s=90, c='g')
    fig.savefig(outpath + 'multidaytrack.pdf', bbox_inches="tight")
    plt.close(fig)
    return 0


def plothr(gpx: tl.GpxReadout, outpath: str):
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


def plotele(gpx: tl.GpxReadout, outpath: str):
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

    multiday = False

    # argument parsing guardabile con tanti controlli che ci sta
    args = tl.parse_args(sys.argv)
    # input path
    if "p" in args:
        if len(args["p"]) != 1:
            multiday = True
        path = args["p"]
    else:
        print("No input file")
        return -1

    # output path
    if "-op" in args:
        if len(args["op"]) != 1:
            print("Too many output paths")
            return -1
        outpath = args["op"]
    else:
        outpath = ''

    # time strings
    if "t" in args:
        timestrings = args["t"]
    else:
        timestrings = []

    # execution
    if not multiday:
        gpx = tl.GpxReadout(path[0])
        plottrack(gpx, outpath, timeinput = timestrings)
        plothr(gpx, outpath)
        plotele(gpx, outpath)
    else:
        gpxs = [tl.GpxReadout(p) for p in path]
        plotmultiday(gpxs, outpath)


if __name__ == "__main__":
    main()

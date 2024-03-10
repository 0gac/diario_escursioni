import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import sys
import datetime
import tools as tl


def plottrack(gpx: tl.GpxReadout, outpath: str, timeinput: np.ndarray = None, verbose = False):
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
    if verbose:
        track_extremes = gpx.get_extremes()
        print("ora di inizio | ora di fine")
        print(track_extremes['exttimes'][0], " | ", track_extremes['exttimes'][1])
    return count_images


def plotmultiday(gpxs: list, outpath: str, verbose=False):
    tracks = []
    tracks_ele = []
    tracks_extremes = []
    for gpx in gpxs:
        tracks.append(gpx.coordinate_raw)
        tracks_ele.append(gpx.ele)
        tracks_extremes.append(gpx.get_extremes())

    maxx = max([max(t[:, 0]) for t in tracks])
    maxy = max([max(t[:, 1]) for t in tracks])

    for t in tracks:
        t[:, 0] = t[:, 0] / maxx
        t[:, 1] = t[:, 1] / maxy

    for te in tracks_extremes:
        # normalization of start/stop coordinates considering all the tracks
        te['startcoords'][0] = te['startcoords_raw'][0] / maxx
        te['startcoords'][1] = te['startcoords_raw'][1] / maxy
        te['endcoords'][0] = te['endcoords_raw'][0] / maxx
        te['endcoords'][1] = te['endcoords_raw'][1] / maxy

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
        ax.scatter(e['startcoords'][1], e['startcoords'][0], s=60, c='k')
        ax.scatter(e['endcoords'][1], e['endcoords'][0], s=60, c='k')
        # adding "notte numero " annotation
        if counter != len(tracks_extremes)-1:
            label = "Notte " +\
                    str(counter + 1) +\
                    "\n" + str(e['extdays'][1].day) +\
                    "/" + str(e['extdays'][1].month) +\
                    "/" + str(e['extdays'][1].year)
            ax.annotate(label, xy=(e['endcoords'][1], e['endcoords'][0]), xytext=(30, 30),
                        textcoords='offset points',
                        color='k', size='large',
                        arrowprops=dict(
                        arrowstyle='simple,tail_width=0.2,head_width=0.8,head_length=0.8',
                        color='k'),
                        weight='bold')
        counter += 1

    fd = [te['extdays'][0] for te in tracks_extremes]  # first days
    ld = [te['extdays'][1] for te in tracks_extremes]  # last days
    endcoords = [te['endcoords'] for te in tracks_extremes]  # end coord for each day
    startcoords = [te['startcoords'] for te in tracks_extremes]  # stard coord for each day

    startcoordstot = [s for s, f in zip(startcoords, fd) if f == min(fd)][0]  # start coord for the first day
    endcoordstot = [e for e, l in zip(endcoords, ld) if l == max(ld)][0]  # end coord for the last day

    ax.scatter(endcoordstot[1],  # end of the last day
               endcoordstot[0],
               s=90, c='r')
    ax.scatter(startcoordstot[1],  # start of the first day
               startcoordstot[0],
               s=90, c='g')

    fig.savefig(outpath + 'multidaytrack.pdf', bbox_inches="tight")
    plt.close(fig)
    if verbose:
        print("ora di inizio | ora di fine")
        for te in tracks_extremes:
            print(te['exttimes'][0], " | ", te['exttimes'][1])
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
    if "op" in args:
        if len(args["op"]) != 1:
            print("Too many output paths")
            return -1
        outpath = args["op"][0]
    else:
        outpath = ''

    # time strings
    if "t" in args:
        timestrings = args["t"]
    else:
        timestrings = []

    # verbose
    if "v" in args:
        verbose = True
    else:
        verbose = False

    # execution
    if not multiday:
        gpx = tl.GpxReadout(path[0])
        plottrack(gpx, outpath, timeinput=timestrings, verbose=verbose)
        plothr(gpx, outpath)
        plotele(gpx, outpath)
    else:
        gpxs = [tl.GpxReadout(p) for p in path]
        plotmultiday(gpxs, outpath, verbose=verbose)


if __name__ == "__main__":
    main()

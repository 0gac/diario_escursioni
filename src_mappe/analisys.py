import sys
import tools as tl
import plotter as pl


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

    # legend position: lower/upper left/right
    if "lp" in args:
        leg_pos = ''
        for w in args['lp']:
            leg_pos += w
            leg_pos += ' '
        leg_pos = leg_pos[:-1]
    else:
        leg_pos = 'lower left'

    # execution
    if not multiday:
        gpx = tl.GpxReadout(path[0])
        pl.plottrack(gpx, outpath, timeinput=timestrings, verbose=verbose, leg_pos=leg_pos)
        pl.plothr(gpx, outpath)
        pl.plotele(gpx, outpath)
    else:
        gpxs = [tl.GpxReadout(p) for p in path]
        pl.plotmultiday(gpxs, outpath, verbose=verbose)


if __name__ == "__main__":
    main()

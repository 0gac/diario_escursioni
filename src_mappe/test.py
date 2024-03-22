import sys
import tools as tl
import matplotlib.pyplot as plt
import plotter as pl

gpx_path = "../relazioni/sciata1703.gpx"

gpx = tl.GpxReadout(gpx_path)
pl.plottrack(gpx, '', manual_img = 3) 

plt.show()
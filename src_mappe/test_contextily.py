import matplotlib.pyplot as plt
import contextily as cx
import tools as tl

fpath = "../relazioni/sciata1703.gpx"
gpx_file = tl.GpxReadout(fpath)

w = min(gpx_file.coordinate_raw[:, 1])
e = max(gpx_file.coordinate_raw[:, 1])
s = min(gpx_file.coordinate_raw[:, 0])
n = max(gpx_file.coordinate_raw[:, 0])

print(w, s, e, n)

img, ext = cx.bounds2img(w, s, e, n, ll=True, zoom = 14, source=cx.providers.OpenTopoMap)
img, ext = cx.warp_tiles(img, ext)


f, ax = plt.subplots(1, figsize=(9, 9))

ax.imshow(img, extent=ext)

plot = ax.scatter(gpx_file.coordinate_raw[:, 1], gpx_file.coordinate_raw[:, 0],s=5)

plt.show()
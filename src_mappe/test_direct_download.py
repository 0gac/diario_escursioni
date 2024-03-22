import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def download_image(url):
    response = requests.get(url)
    print(f"Downloading from {url}...")
    # url = url.replace("/", "_").replace(":", "_")
    url = "your_image.png"
    with open(f"{url}", "wb") as file:
        file.write(response.content)

url = "https://opentopomap.org/16/46348/11453"

download_image(url)

img = mpimg.imread('your_image.png')
imgplot = plt.imshow(img)
plt.show()
import numpy as np
import pandas as pd
import cv2

# Load the image
image_path = "camera/image_15.jpg"
frame = cv2.imread(image_path)
if frame is None:
    print("Error loading image.")
    exit()

# Optional: Resize for faster computation
frame = cv2.resize(frame, (200, 200))

# Split the image into its BGR channels
blue_channel = frame[:, :, 0].flatten()
green_channel = frame[:, :, 1].flatten()
red_channel = frame[:, :, 2].flatten()

# Compute the median for each channel
b_median = int(np.median(blue_channel))
g_median = int(np.median(green_channel))
r_median = int(np.median(red_channel))

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if (d <= minimum):
            minimum = d
            cname = df.loc[i, 'color_name'] + '   Hex=' + df.loc[i, 'hex']
    return cname

color_info = getColorName(r_median, g_median, b_median)
print("Median color in the image:", color_info)
print("Red: ", r_median, ", Green: ", g_median, ", Blue: ", b_median)



import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

known_rgb =np.array([[255,201,103], [254,185,110], [253,167,118], [252,148,126], [251,130,134], [250,113,142], [249,97,151], [248,82,160]])
known_ph = np.array([6.8,7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2])

new_median_rgb = [200,237,100]

distances = np.linalg.norm(known_rgb - new_median_rgb, axis=1)

closest_index = np.argmin(distances)

predicted_ph = known_ph[closest_index]

print(f"Predicted pH value: {predicted_ph: .2f}")




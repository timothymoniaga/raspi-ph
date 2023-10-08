
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

X = [[255,201,103], [254,185,110], [253,167,118], [252,148,126], [251,130,134], [250,113,142], [249,97,151], [248,82,160]]
y = [6.8,7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

model = LinearRegression().fit(X_train, y_train)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae: .2f}")

new_median_rgb = [100,230,229]

predicted_ph = model.predict([new_median_rgb])[0]

print(f"Predicted pH value: {predicted_ph: .2f}")




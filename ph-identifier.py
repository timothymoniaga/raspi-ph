import os 
import picamera
import pygame
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import RPi.GPIO as GPIO

# For 5x5 cm picture (25cm^2)
if not os.path.exists('images'):
    os.makedirs('images')

def capture_image (filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (2464,2464)
        camera.awb_mode = 'auto'
        camera.brightness = 55
        camera.contrast = 10
        camera.saturation = -5
        camera.sharpness = 10
        camera.iso = 100
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'

        camera.start_preview()
        print("Press 's' to save the image...")

        pygame.init()

        screen = pygame.display.set_mode([1024,768])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        camera.capture(filename)
                        running = False
                    if event.key == pygame.K_ESCAPE:
                        running = False
        camera.stop_preview()
        pygame.quit()

def get_colour (filename):
    frame = cv2.imread(filename)
    if frame is None:
        print("Error loading image")
        exit()

    frame = cv2.resize(frame, (200,200))

    blue_channel = frame[:, :, 0].flatten()
    green_channel = frame [:, :, 1].flatten()
    red_channel = frame [:, :, 2].flatten()

    b_median = int(np.median(blue_channel))
    g_median = int(np.median(green_channel))
    r_median = int(np.median(red_channel))

    return([r_median, g_median, b_median])


def estimate_ph (new_rgb):
    known_rgb = np.array([
        [225,201,103],
        [254,185,110],
        [253,167,118],
        [252,148,126],
        [251,130,134],
        [250,113,142],
        [249,97,151],
        [248,82,160]
        ])
    known_ph = np.array([6.8,7.0,7.2,7.4,7.6,7.8,8.0,8.2])

    distances = np.linalg.norm(known_rgb - new_rgb, axis=1)

    closest_index = np.argmin(distances)

    predicted_ph = known_ph[closest_index]

    return(round(predicted_ph, 1))

def start_pumps ():
    GPIO.setmode(GPIO.BCM)
    pin_number = 18 #subject to change
    GPIO.setup(pin_number, GPIO.OUT)

    try:
        while True:
            command = input("Enter 'on' to turn on, 'off' to turn off, 'quit' to exit: ")

            if command =="on":
                GPIO.output(pin_number, GPIO.HIGH)
                print("GPIO pin turned on!")

            elif command == "off":
                GPIO.output(pin_number, GPIO.LOW)
                print("GPIO pin turned off!")

            elif ccommand == "quit":
                break
            else:
                print("Invalid command. Try again.")


if __name__ == "__main__":

    start_pumps()
    input("Press enter to take image and read PH")
    num_files = len(os.listdir('images'))
    filename = f"images/image{num_files +1}.jpg"
    capture_image(filename)
    rgb = get_colour(filename)
    print(estimate_ph(rgb))



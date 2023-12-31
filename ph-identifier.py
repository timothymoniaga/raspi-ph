import os 
import picamera
import pygame
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import RPi.GPIO as GPIO
import time

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

def pin_pwm_time(pin_number, timer, power):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)
    pwm = GPIO.PWM(pin_number, 100)
    pwm.start(0)
    
    duty_cycle = float(power)
    pwm.ChangeDutyCycle(duty_cycle)

    # hardcoded for the LED pin
    if pin_number == 12:
        print("calculationg values...")
        # call image taking and calculation functions

    time.sleep(timer)

    GPIO.cleanup()
    pwm.stop()

def pin_on(pin_number, on_flag):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)
    
    if on_flag:
        GPIO.output(pin_number, GPIO.HIGH)

    else: 
        GPIO.output(pin_number, GPIO.LOW)




def start_pumps ():
    sample_pump = 26 #sample water
    led = 12 
    dosing_pump = 13
    washing_pump = 6
    mixing_pump = 5
    valve = 16 #this is the bottom where we get rif of the water


    #sequence
    # sample pump on
    # sample pump off
    # dosing pump on
    # dosing pump off
    # mixing pump on 
    # mixing pump off
    # close valve
    # turn LED on 
    # take image
    # turn LED off
    # calculate PH
    # open valve
    # washing pump on
    # washing pump off

    try:
        # close the valve
        pin_on(valve, False)
        # sample pump
        pin_pwm_time(sample_pump, 5, 75) # on/off no need pwm
        # dosing pump
        pin_pwm_time(dosing_pump, 2.7, 12.5)
        # mixing pump
        pin_pwm_time(mixing_pump, 10, 100) 
        #LED
        pin_pwm_time(led, 5, 10)
        # Image and calculation is taken inside the pwm pin function

        # open valve
        pin_on(valve, True)

        # washing pump
        pin_pwm_time(washing_pump, 15, 100)


    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":

    start_pumps()
    input("Press enter to take image and read PH")
    num_files = len(os.listdir('images'))
    filename = f"images/image{num_files +1}.jpg"
    capture_image(filename)
    rgb = get_colour(filename)
    print(estimate_ph(rgb))



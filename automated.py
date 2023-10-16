import RPi.GPIO as GPIO
import time
import picamera
import cv2
import numpy as np
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

if not os.path.exists('photos'):
    os.makedirs('photos')

def digital_for_duration(pin, duration):
    # If duration is zero, turn on the pin and return immediately
    if duration == 0:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        print(f"Pin {pin} turned on indefinitely.")
        return

    # For the Washing pump
    if pin == 21:
        GPIO.setup(20, GPIO.OUT)  # Set up the Valve & pump-out pin
        GPIO.output(20, GPIO.HIGH)  # Open the Valve
        print("Valve (Pin 20) opened.")
    
    # For the Sample water
    elif pin == 23:
        GPIO.setup(20, GPIO.OUT)  # Set up the Valve & pump-out pin
        GPIO.output(20, GPIO.LOW)  # Close the Valve
        print("Valve (Pin 20) closed.")
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    print(f"Pin {pin} turned on for {duration} seconds.")
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print(f"\nInterrupted! Turning off pin {pin} immediately.")
    
    GPIO.output(pin, GPIO.LOW)
    print(f"Pin {pin} turned off.")


def pwm_for_duration(pin, duty_cycle, duration):
    GPIO.setup(pin, GPIO.OUT)
    
    pwm = GPIO.PWM(pin, 100)  # Frequency is hardcoded to 100Hz
    
    try:
        pwm.start(duty_cycle)
        print(f"Started PWM on pin {pin} with 100Hz frequency and {duty_cycle}% duty cycle.")
        print(f"It will run for {duration} seconds or you can press Ctrl+C to exit early.")
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\nExiting early due to user interrupt.")
    finally:
        pwm.stop()
        print(f"Stopped PWM on pin {pin}.")

def turn_on_led_indefinitely():
    pin = 12
    duty_cycle = 40
    GPIO.setup(pin, GPIO.OUT)
    
    pwm = GPIO.PWM(pin, 100)  # Frequency is hardcoded to 100Hz
    pwm.start(duty_cycle)
    print(f"LED (Pin {pin}) turned on indefinitely with {duty_cycle}% duty cycle.")


def sample_water():
    digital_for_duration(23, 1.7)

def dosing_pump():
    pwm_for_duration(13, 25, 3.5)

def mixing_pump():
    digital_for_duration(16, 3)

def turn_on_led():
    pwm_for_duration(12, 3, 0)  # Assuming you want the LED to stay on indefinitely

def capture_image():

    num_files = len(os.listdir('photos'))
    filename = f"photos/image{num_files + 1}.jpg"

    with picamera.PiCamera() as camera:
        camera.resolution = (2464, 2464)
        camera.awb_mode = 'auto'
        camera.brightness = 55
        camera.contrast = 10
        camera.saturation = -5
        camera.sharpness = 10
        camera.iso = 100
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'
        
        # Capture the image immediately
        camera.start_preview()
        time.sleep(2)  # Let the camera adjust for 2 seconds
        camera.capture(filename)
        camera.stop_preview()
        print(f"Captured image saved as: {filename}")

        

        return filename
        # Display the captured image
        # img = cv2.imread(filename)
        # cv2.imshow('Captured Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

def get_median_rgb(filename):
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

def estimate_ph_value(rgb_values):
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

    distances = np.linalg.norm(known_rgb - rgb_values, axis=1)

    closest_index = np.argmin(distances)

    predicted_ph = known_ph[closest_index]

    return(round(predicted_ph, 1))

def washing_pump():
    digital_for_duration(21, 1) 
    time.sleep(3)
    digital_for_duration(21,3)

def run_sequence():
    try:
        sample_water()
        dosing_pump()
        mixing_pump()
        #turn_on_led_indefinitely()
        pin = 12
        duty_cycle = 40
        GPIO.setup(pin, GPIO.OUT)
        
        pwm = GPIO.PWM(pin, 100)  # Frequency is hardcoded to 100Hz
        pwm.start(duty_cycle)
        print(f"LED (Pin {pin}) turned on indefinitely with {duty_cycle}% duty cycle.")
        
        filename = capture_image()
        
        rgb_values = get_median_rgb(filename)
        ph_value = estimate_ph_value(rgb_values)
        print(f"Estimated pH: {ph_value}")
        
        washing_pump()
    except KeyboardInterrupt:
        print("\nSequence interrupted by user.")



def main():
    try:
        while True:
            print("\nMenu:")
            print("1. Digital Output")
            print("2. PWM Output")
            print("3. Sequence")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                print("\nDigital Output Options:")
                print("1. Sample water (Pin 23)")
                print("2. Washing pump (Pin 21)")
                print("3. Mixing pump (Pin 16)")
                print("4. Valve (Pin 20)")
                
                digital_choice = input("Enter your choice: ")
                if digital_choice == "1":
                    pin = 23
                elif digital_choice == "2":
                    pin = 21
                elif digital_choice == "3":
                    pin = 16
                elif digital_choice == "4":
                    pin = 20
                else:
                    print("Invalid choice. Returning to main menu.")
                    continue

                duration = float(input("Enter duration in seconds: "))
                digital_for_duration(pin, duration)
                
            elif choice == "2":
                print("\nPWM Output Options:")
                print("1. LED (Pin 12, max 40%)")
                print("2. Dosing pump (Pin 13, max 40%)")
                
                pwm_choice = input("Enter your choice: ")
                if pwm_choice == "1":
                    turn_on_led_indefinitely()
                    continue
                elif pwm_choice == "2":
                    pin = 13
                else:
                    print("Invalid choice. Returning to main menu.")
                    continue

                duty_cycle = float(input("Enter duty cycle (0-40): "))
                if duty_cycle > 40:
                    print("Duty cycle exceeds maximum limit. Setting to 40%.")
                    duty_cycle = 40

                duration = float(input("Enter duration in seconds: "))
                pwm_for_duration(pin, duty_cycle, duration)

            elif choice == "3":
                run_sequence()
                
            elif choice == "4":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
        GPIO.cleanup()



if __name__ == "__main__":
    main()

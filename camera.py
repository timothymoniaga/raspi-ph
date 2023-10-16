import os
import picamera 
import pygame
import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_PIN = 12
GPIO.setup(LED_PIN, GPIO.OUT)

if not os.path.exists('camera'):
    os.makedirs('camera')

def capture_image(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.awb_mode = 'auto'
        camera.brightness = 55
        camera.contrast = 10
        camera.saturation = -5
        camera.sharpness = 10
        camera.iso = 200
        camera.exposure_compensation = 0
        camera.exposure_mode = 'auto'
        camera.meter_mode = 'average'

        # Turn on the LED
        GPIO.output(LED_PIN, GPIO.HIGH)

        camera.start_preview()
        print("press 's' to save the image...")

        pygame.init()
        screen = pygame.display.set_mode([1024,768])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        camera.capture(filename)
                        print(f"Image saved to {filename}")
                        running = False
        camera.stop_preview()

        # Turn off the LED
        GPIO.output(LED_PIN, GPIO.LOW)

        pygame.quit()

if __name__ == "__main__":
    num_files = len(os.listdir('camera'))
    filename = f"camera/image_{num_files + 1}.jpg"
    capture_image(filename)

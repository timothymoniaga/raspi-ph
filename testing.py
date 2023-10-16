import RPi.GPIO as GPIO
import time

def digital_for_duration(pin, duration):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    
    try:
        GPIO.output(pin, GPIO.HIGH)
        print(f"Pin {pin} turned ON for {duration} seconds. Press Ctrl+C to exit early.")
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\nExiting early due to user interrupt.")
    finally:
        GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()
        print(f"Pin {pin} turned OFF.")

def pwm_for_duration(pin, duty_cycle, duration):
    GPIO.setmode(GPIO.BCM)
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
        GPIO.cleanup()
        print(f"Stopped PWM on pin {pin}.")

def main():
    try:
        while True:
            print("\nMenu:")
            print("1. Digital Output")
            print("2. PWM Output")
            print("3. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                print("\nDigital Output Options:")
                print("1. Sample water (Pin 23)")
                print("2. Washing pump (Pin 21)")
                print("3. Mixing pump (Pin 16)")
                print("4. Valve & pump-out (Pin 20)")
                
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
                    pin = 12
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
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
        GPIO.cleanup()

if __name__ == "__main__":
    main()

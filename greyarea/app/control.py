from app import app
import time


# PID Tuning Constants
P = 40
I = 10
D = 0


# GPIO Configuration
if app.config['GPIO']:
    import RPi.GPIO as GPIO
else:
    from app.mock import GPIO


# OneWire Therm Sensor Configuration
if app.config['ONEWIRE']:
    from w1thermsensor import W1ThermSensor
else:
    from app.mock import W1ThermSensor


# External Values, Read-Only
Setpoint = 140.0
Run = True

# Hardware Values, Read-Write
Temp = 138.0
RelayState = True


def controlworker():
    global Setpoint
    global Run
    global Temp
    global RelayState

    relay = int(app.config['RELAYPIN'])
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay, GPIO.OUT, initial=GPIO.LOW)

    sensor = W1ThermSensor()

    lasterror = 0.0
    errori = 0.0
    errord = 0.0
    result = 0.0

    while True:
        # Read latest values from the UI
        setpoint = Setpoint
        run = Run

        # Process
        ## Read values from hardware
        temp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        if run:
            # P
            currenterror = setpoint - temp

            # Sum and cap I
            errori += currenterror
            if errori > 50:
                errori = 50
            elif errori < -50:
                errori = -50

            # Calculate D
            errord = currenterror - lasterror

            # Calculate and cap PID
            result = (P * currenterror) + (I * errori) + (D * errord)
            if result > 500:
                result = 500
            elif result < -500:
                result = -500

            # Set relay state
            if result > 0:
                GPIO.output(relay, GPIO.HIGH)
            else:
                GPIO.output(relay, GPIO.LOW)
        else:
            GPIO.output(relay, GPIO.LOW)
            lasterror = 0.0
            errori = 0.0
            errord = 0.0
            result = 0

        # Publish values
        Temp = temp
        RelayState = bool(GPIO.input(relay))

        # Sleep
        time.sleep(5)


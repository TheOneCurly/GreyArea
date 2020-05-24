from app import app
from gpiozero import OutputDevice
import time

# PID Tuning Constants
P = 40
I = 10
D = 0

# GPIO Configuration
if app.config['GPIO']:
    from gpiozero.pins.rpigpio import RPiGPIOFactory
    Factory = RPiGPIOFactory()
else:
    from gpiozero.pins.mock import MockFactory
    Factory = MockFactory()

class Relay(OutputDevice):
    def __init__(self, pin):
        OutputDevice.__init__(self, pin=pin, active_high=True, initial_value=False, pin_factory=Factory)

# OneWire Therm Sensor Configuration
if app.config['ONEWIRE']:
    from w1thermsensor import W1ThermSensor
else:
    class W1ThermSensor():
        DEGREES_F = 0x02

        def __init__(self):
            self.moctemp = 140

        def get_temperature(self, unit):
            return self.moctemp


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

    relay = Relay(app.config['RELAYPIN'])
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
                relay.on()
            else:
                relay.off()
        else:
            lasterror = 0.0
            errori = 0.0
            errord = 0.0
            result = 0

        # Publish values
        Temp = temp
        RelayState = bool(relay.value)

        # Sleep
        time.sleep(5)


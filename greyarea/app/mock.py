class GPIO():
    BCM = 11
    OUT = 0
    LOW = 0
    HIGH = 1

    def setmode(mode):
        pass

    def setup(channel, mode, initial):
        pass

    def output(channel, state):
        pass

    def input(channel):
        return 1

class W1ThermSensor():
    DEGREES_F = 0x02

    def __init__(self):
        self.moctemp = 140

    def get_temperature(self, unit):
        return self.moctemp

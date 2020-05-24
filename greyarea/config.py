class Config(object):
    GPIO = False
    ONEWIRE = False
    RELAYPIN=17

class DevConfig(Config):
    GPIO = False
    ONEWIRE = False

class ProdConfig(Config):
    GPIO = True
    ONEWIRE = True

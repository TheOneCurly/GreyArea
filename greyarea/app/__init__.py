from flask import Flask
from config import DevConfig, ProdConfig
import threading

app = Flask(__name__)
app.config.from_object(DevConfig)

from app import routes, control, mock

# Start the control thread if it isn't running
if "ControlThread" not in [thread.name for thread in threading.enumerate()]:
    controlthread = threading.Thread(target=control.controlworker, name="ControlThread", daemon=True)
    controlthread.start()

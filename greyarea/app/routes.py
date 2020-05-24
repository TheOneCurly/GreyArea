from flask import send_from_directory, render_template, request, Response, json, redirect
from app import app
import app.control as control

@app.route('/')
def index():
    return render_template('index.html', setpoint=control.Setpoint, run=control.Run, temp=control.Temp, relay=control.RelayState)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/scripts/<path:path>')
def send_script(path):
    return send_from_directory('scripts', path)


@app.route('/setpoint', methods=['POST'])
@app.route('/setpoint/', methods=['POST'])
def serve_setpoint():
    if 'setpoint' in request.form:
        try: 
            control.Setpoint = int(request.form['setpoint'])
        except ValueError:
            print("Setpoint not an int, ignoring.")

    return redirect('/')

@app.route('/run', methods=['POST'])
@app.route('/run/', methods=['POST'])
def serve_run():
    control.Run = not control.Run
    return redirect('/')


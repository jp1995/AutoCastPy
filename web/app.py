from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from utility.logging_setup import log
import socket
import os


def run_webserver(q):
    os.chdir('./web/')
    app = Flask(__name__, template_folder='.', static_folder='assets')
    socketio = SocketIO(app, cors_allowed_origins='*')
    port = 5001

    log.info("Webserver started")
    log.info(f"* Running on http://127.0.0.1:{port}\n"
             f"* Running on http://{get_local_ip()}:{port}\n")

    @app.route('/')
    def index():
        render_table = render_template('index.html')
        return render_table

    @app.route('/receive_data', methods=['POST'])
    def receive_data():
        data = request.json
        q.put(data)
        return jsonify({"message": "Data received successfully!"})

    socketio.run(app, host='0.0.0.0', port=port)


def get_local_ip():
    ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ts.settimeout(0)
    try:
        ts.connect(("1.1.1.1", 1))
    except (socket.gaierror, OSError):
        pass
    finally:
        localIP = ts.getsockname()[0]
        ts.close()
    return localIP

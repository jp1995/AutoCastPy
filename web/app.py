from flask import Flask, render_template
import socket
import json
import os

data = None
matchData = []
playlistData = None


def run_webserver(mmrq, matchq, playlistq):
    os.chdir('./web/')
    app = Flask(__name__, template_folder='.', static_folder='assets')
    app.jinja_env.auto_reload = True

    log.info("Webserver started")
    log.info("* Running on http://127.0.0.1:5000\n"
             f"* Running on http://{get_local_ip()}:5000\n")

    @app.route('/')
    def index():
        render_table = render_template('index.html')
        return render_table

    app.run()


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

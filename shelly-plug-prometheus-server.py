#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
from flask import Flask, Response, request

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Web server that publishes the output of Shelly Plug power for Prometheus')

parser.add_argument('--shelly_user',
                    type=str,
                    help="user credentials for the Shelly Plug",
                    default='admin')

parser.add_argument('--shelly_pass',
                    type=str,
                    help="pass credentials for the Shelly Plug",
                    default='admin')

parser.add_argument('--port',
                    type=int,
                    help = "listen port for this server",
                    default='9440')

def start_server(port):
    app.run(host='0.0.0.0', port=port, debug=False)


def main():
    args = parser.parse_args()

    app.config['shelly_user'] = args.shelly_user
    app.config['shelly_pass'] = args.shelly_pass

    print("starting server at port: %d" % args.port)
    start_server(args.port)


def get_shelly_power_reading(shelly_address):
    shelly_user = app.config['shelly_user']
    shelly_pass = app.config['shelly_pass']

    r = requests.get('http://%s/meter/0' % shelly_address, auth=(shelly_user, shelly_pass))
    power = 0
    if r.status_code == 200:
        power = r.json()['power']
    return power
        

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/metrics")
def metrics():

    shelly_address = request.args.get('shelly_address')
    
    response = '\n'.join(['# HELP {metric} Instantaneous power reading (W)',
                          '# TYPE {metric} gauge',
                          '{metric} {power}'])
    return Response(response.format(metric='shelly_plug_power',
                                    power=get_shelly_power_reading(shelly_address)),
                                    mimetype='text/plain')

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import yaml
from flask import Flask, Response

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Web server that publishes the output of Shelly Plug power for Prometheus')

parser.add_argument('--shelly_address',
                    type=str,
                    required=True,
                    help="IP or host address of the Shelly Plug")

parser.add_argument('--shelly_credentials_file',
                    type=str,
                    required=True,
                    help="yaml file containing credentials for the Shelly Plug")

parser.add_argument('--port',
                    type=int,
                    help = "listen port for this server",
                    default = '9440')

def start_server(port):
    app.run(host='0.0.0.0', port=port, debug=False)


def main():
    args = parser.parse_args()

    shelly_credentials = yaml.load(open(args.shelly_credentials_file))
    
    app.config['shelly_address'] = args.shelly_address
    app.config['shelly_user'] = shelly_credentials['user']
    app.config['shelly_pass'] = shelly_credentials['pass']

    print("starting server at port: %d" % args.port)
    start_server(args.port)


def get_shelly_power_reading():
    shelly_address = app.config['shelly_address']
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
    response = '\n'.join(['# HELP {metric} Instantaneous power reading (W)',
                          '# TYPE {metric} gauge',
                          '{metric} {power}'])
    return Response(response.format(metric='shelly_plug_power', power=get_shelly_power_reading()), mimetype='text/plain')

if __name__ == '__main__':
    main()

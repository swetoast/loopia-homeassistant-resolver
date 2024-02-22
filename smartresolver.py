from flask import Flask, jsonify, redirect, url_for
import requests
import configparser
import os

app = Flask(__name__)

def get_external_ip():
    return requests.get('https://api.ipify.org').text

def update_dyndns(username, password, hostnames):
    url = "https://dns.loopia.se/XDynDNSServer/XDynDNS.php"
    ip_address = get_external_ip()
    results = []
    for hostname in hostnames:
        params = {
            "hostname": hostname,
            "myip": ip_address,
            "wildcard": "NOCHG"
        }
        response = requests.get(url, params=params, auth=(username, password))
        result = {
            "hostname": hostname,
            "ip_address": ip_address,
            "status": response.text
        }
        results.append(result)
    return results

@app.route('/update_dyndns')
def dyndns_update():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'dns_endpoint.conf')
    config.read(config_path)
    username = config.get('Credentials', 'username')
    password = config.get('Credentials', 'password')
    hostnames = config.get('Hostnames', 'hostnames').split(', ')
    results = update_dyndns(username, password, hostnames)
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('dyndns_update')), 302

if __name__ == '__main__':
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'dns_endpoint.conf')
    config.read(config_path)
    host = config.get('DEFAULT', 'HOST')
    port = config.getint('DEFAULT', 'PORT')
    use_https = config.getboolean('DEFAULT', 'USE_HTTPS')
    certificate_path = config.get('DEFAULT', 'CERTIFICATE_PATH')
    key_path = config.get('DEFAULT', 'KEY_PATH')

    if use_https:
        if os.path.exists(certificate_path) and os.path.exists(key_path):
            app.run(host=host, port=port, ssl_context=(certificate_path, key_path))
        else:
            app.run(host=host, port=port)
    else:
        app.run(host=host, port=port)

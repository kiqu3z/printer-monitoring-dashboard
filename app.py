from flask import Flask, render_template
from monitor_printer import get_printer_data
import logging

app = Flask(__name__)

@app.route('/')
def index():
    user = 'User'
    auth_key = 'auth_key'
    priv_key = 'priv_key'

    printer1 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'X4220RX')
    printer2 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'X4220RX')
    printer3 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'C4062FX')
    printer4 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'C4062FX')
    printer5 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'M4080FX')
    printer6 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'E57540')

    return render_template('index.html', printer1=printer1, printer2=printer2, printer3=printer3, printer4=printer4, printer5=printer5, printer6=printer6)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)

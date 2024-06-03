# Printer Monitoring Dashboard

## Overview

This Printer Monitoring Dashboard is a web application designed to monitor the status and ink levels of multiple networked printers. The dashboard provides real-time information about the operational status and the levels of cyan, magenta, yellow, and black inks (where applicable).

## Features

- Monitor the status of each printer.
- Display ink levels for cyan, magenta, yellow, and black inks.
- Support for different models of printers.
- Compact and user-friendly interface.

## Prerequisites

- Python 3.x
- `pysnmp` library
- `flask` library

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/kiqu3z/printer-monitoring-dashboard.git
    cd printer-monitoring-dashboard
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

### Update Printer Information

Edit the `monitor_printer.py` file to include the correct OIDs for each printer model. Ensure that the IP addresses and OIDs match the printers you want to monitor.

```python
# Example OID configuration for different printer models
if model == 'X4220RX':
    cyan_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'
    magenta_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'
    yellow_oid = '1.3.6.1.2.1.43.11.1.1.9.1.3'
    black_oid = '1.3.6.1.2.1.43.11.1.1.9.1.4'
    color_max_value = 20000  # Adjust this value as needed
    black_max_value = 32258  # Adjust this value as needed
```


### Set User Credentials

Edit the app.py file to set the SNMP user credentials.

```python
user = 'User'
auth_key = 'auth_key'
priv_key = 'priv_key'
```

### Running the Application
#### 1. Start the Flask server:

```bash
python app.py
```

#### 2. Open the dashboard in your browser:

Navigate to http://127.0.0.1:5000 in your web browser to view the dashboard.


### File Structure

- app.py: Main Flask application file that sets up the server and routes.
- monitor_printer.py: Contains the logic for fetching SNMP data from the printers.
- templates/index.html: HTML template for the dashboard.
- static/styles.css: CSS file for styling the dashboard.


### Customization

#### Adding New Printers
To add new printers, update the app.py and monitor_printer.py files with the new printer details and OIDs.

#### Styling
Customize the static/styles.css file to change the appearance of the dashboard.

#### Troubleshooting
#### SNMP Errors
Ensure that the SNMP community string and OIDs are correct and that the printers are configured to respond to SNMP queries.

#### Flask Server Issues
Ensure all dependencies are installed and that the virtual environment is activated (if used).

#### License
This project is licensed under the MIT License. See the LICENSE file for details.

#### Contributing
Feel free to submit issues, fork the repository, and send pull requests for any improvements or bug fixes.

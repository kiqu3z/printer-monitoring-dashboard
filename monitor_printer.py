import logging
from pysnmp.hlapi import *
from pysnmp.proto.rfc1905 import NoSuchObject, NoSuchInstance

logging.basicConfig(level=logging.INFO)

def get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, oid):
    logging.info(f'Consultando OID {oid} no IP {ip}')
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(user, authKey=auth_key, privKey=priv_key, authProtocol=auth_protocol, privProtocol=priv_protocol),
        UdpTransportTarget((ip, 161), timeout=1, retries=5),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        logging.error(f'Erro SNMP: {errorIndication}')
        return None
    elif errorStatus:
        logging.error(f'Erro de status SNMP: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
        return None
    else:
        for varBind in varBinds:
            value = varBind[1]
            if isinstance(value, (NoSuchObject, NoSuchInstance)):
                logging.error(f'OID {oid} não encontrado no IP {ip}')
                return None
            return int(value)  # Converter para inteiro

def calculate_percentage(value, max_value):
    return min(max(int((value / max_value) * 100), 0), 100) if value is not None else 0

def get_printer_data(ip, user, auth_key, priv_key, model):
    auth_protocol = usmHMACMD5AuthProtocol
    priv_protocol = usmAesCfb128Protocol

    status_oid = '1.3.6.1.2.1.25.3.2.1.5.1'
    if model == 'X4220RX':
        cyan_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'
        magenta_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'
        yellow_oid = '1.3.6.1.2.1.43.11.1.1.9.1.3'
        black_oid = '1.3.6.1.2.1.43.11.1.1.9.1.4'
        color_max_value = 20000  # Valor máximo para as cores na X4220RX
        black_max_value = 22777  # Valor máximo para o preto na X4220RX
    elif model == 'C4062FX':
        cyan_oid = '1.3.6.1.2.1.43.11.1.1.9.1.1'
        magenta_oid = '1.3.6.1.2.1.43.11.1.1.9.1.2'
        yellow_oid = '1.3.6.1.2.1.43.11.1.1.9.1.3'
        black_oid = '1.3.6.1.2.1.43.11.1.1.9.1.4'
        color_max_value = 10000  # Valor máximo para as cores na C4062FX
        black_max_value = 15000  # Valor máximo para o preto na C4062FX
    elif model == 'M4080FX':
        black_oid = '1.3.6.1.4.1.2690.1.5.3.2.1.1.1.1.7.1.4'
        black_max_value = 15000  # Valor máximo para o preto na M4080FX
    elif model == 'E57540':
        cyan_oid = '1.3.6.1.4.1.253.8.53.13.2.1.1.8.1.3'
        magenta_oid = '1.3.6.1.4.1.253.8.53.13.2.1.1.8.1.4'
        yellow_oid = '1.3.6.1.4.1.253.8.53.13.2.1.1.8.1.5'
        black_oid = '1.3.6.1.4.1.253.8.53.13.2.1.1.8.1.2'
        color_max_value = 10000  # Valor máximo para as cores na E57540
        black_max_value = 15000  # Valor máximo para o preto na E57540

    status_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, status_oid)

    if model == 'M4080FX':
        black_level_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, black_oid)
        black_level = calculate_percentage(black_level_raw, black_max_value)
        return {
            'status': status_raw,
            'cyan_level': 0,
            'magenta_level': 0,
            'yellow_level': 0,
            'black_level': black_level
        }

    cyan_level_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, cyan_oid)
    magenta_level_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, magenta_oid)
    yellow_level_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, yellow_oid)
    black_level_raw = get_snmp_data(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, black_oid)

    status_map = {
        1: 'Outro',
        2: 'Desligado',
        3: 'Desligando',
        4: 'Falha',
        5: 'Ocioso',
        6: 'Imprimindo'
    }
    status = status_map.get(status_raw, 'Desconhecido') if status_raw is not None else 'Desconhecido'

    cyan_level = calculate_percentage(cyan_level_raw, color_max_value)
    magenta_level = calculate_percentage(magenta_level_raw, color_max_value)
    yellow_level = calculate_percentage(yellow_level_raw, color_max_value)
    black_level = calculate_percentage(black_level_raw, black_max_value)

    return {
        'status': status,
        'cyan_level': cyan_level,
        'magenta_level': magenta_level,
        'yellow_level': yellow_level,
        'black_level': black_level
    }

if __name__ == '__main__':
    user = 'user'
    auth_key = 'auth_key'
    priv_key = 'priv_key'

    printer1 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'X4220RX')
    printer2 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'X4220RX')
    printer3 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'C4062FX')
    printer4 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'C4062FX')
    printer5 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'M4080FX')
    printer6 = get_printer_data('192.168.0.1', user, auth_key, priv_key, 'E57540')

    print("Printer 1:", printer1)
    print("Printer 2:", printer2)
    print("Printer 3:", printer3)
    print("Printer 4:", printer4)
    print("Printer 5:", printer5)
    print("Printer 6:", printer6)

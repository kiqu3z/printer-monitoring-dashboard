from pysnmp.hlapi import *

def test_snmp(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, oid):
    iterator = getCmd(
        SnmpEngine(),
        UsmUserData(user, authKey=auth_key, privKey=priv_key, authProtocol=auth_protocol, privProtocol=priv_protocol),
        UdpTransportTarget((ip, 161), timeout=1, retries=5),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f'Erro SNMP: {errorIndication}')
    elif errorStatus:
        print(f'Erro de status SNMP: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
    else:
        for varBind in varBinds:
            print(f'{varBind[0]} = {varBind[1]}')

if __name__ == "__main__":
    ip = '192.168.0.1'
    user = 'User'
    auth_key = 'auth_key'
    priv_key = 'priv_key'
    oid = '1.3.6.1.2.1.1.1.0'  # OID padrão para SysDescr

    auth_protocol = usmHMACMD5AuthProtocol
    priv_protocol = usmAesCfb128Protocol

    print(f'Testando com Auth Protocol: MD5, Priv Protocol: AES')
    test_snmp(ip, user, auth_key, priv_key, auth_protocol, priv_protocol, oid)

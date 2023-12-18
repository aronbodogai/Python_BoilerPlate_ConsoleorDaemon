import ipaddress
import socket
from time import sleep

def arbitraryTestFunc(x):
    sleep(.1)
    return (x % 5 ==0)

def isIP(string):
    bool = False
    try:
        if  isinstance(string,int):
            return False
        ip = ipaddress.ip_address(string)
        return True
    except:
        return bool

def resolve_dns(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return hostname,"success", ip_address
    except socket.gaierror as e:
        return hostname,"fail", str(e)
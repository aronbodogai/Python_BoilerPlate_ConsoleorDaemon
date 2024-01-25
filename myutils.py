import ipaddress
import socket
from time import sleep
import logging 


def arbitraryTestFunc(x):
    sleep(.1)
    asd = "not " if (x % 5 !=0) else ""
    logging.info("x is {} and it is {}divisible by 5".format(x,asd))
    return x,(x % 5 ==0)

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
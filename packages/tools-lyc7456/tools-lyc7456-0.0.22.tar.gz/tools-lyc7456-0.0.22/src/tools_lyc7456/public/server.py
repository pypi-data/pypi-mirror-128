import socket

def getMyIP():
    '''获取本机IP地址'''
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print(hostname)
    print(ip)
    return ip
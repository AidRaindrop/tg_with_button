from ping3 import ping, verbose_ping

def setping(ip):

    res = verbose_ping(ip, size = 56)
    return res

#print(res)
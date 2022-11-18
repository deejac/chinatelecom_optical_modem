import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket
from guangmao import guangmao
import sys


def get_host_ip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

    



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gm = guangmao(sys.argv[1:])
    gm.update_remote_desktop()

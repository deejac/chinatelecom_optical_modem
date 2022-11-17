import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket
from guangmao import guangmao



def get_host_ip():
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8',80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    ip = get_host_ip()
    ip = '192.168.1.8'
    #srvname = 'rd'
    srvname = 'rd_test'
    client = ip
    #exPort = '3389'
    #inPort = '3389'
    exPort = '1234'
    inPort = '1234'
    print(ip)
    LOGIN_URL = 'http://192.168.1.1/cgi-bin/luci'
    # get_url为使用cookie所登陆的网址，该网址必须先登录才可
    #username=useradmin&psd=bqfnn
    get_url = 'http://192.168.1.1/cgi-bin/luci/admin/allInfo'
    values = {'username': 'useradmin', 'psd': '*****'}
    postdata = urllib.parse.urlencode(values).encode()
    user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36' \
                 r' (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    # 将cookie保存在本地，并命名为cookie.txt
    cookie_filename = 'cookie.txt'
    cookie_aff = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie_aff)
    opener = urllib.request.build_opener(handler)

    request = urllib.request.Request(LOGIN_URL, postdata, headers)
    try:
        response = opener.open(request)
    except urllib.error.URLError as e:
        print(e.reason)

    cookie_aff.save(ignore_discard=True, ignore_expires=True)

    for item in cookie_aff:
        print('Name =' + item.name)
        print('Value =' + item.value)
    # 使用cookie登陆get_url
    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    print(get_response.read().decode())

    get_url = 'http://192.168.1.1/cgi-bin/luci/admin/settings/pmDisplay'


    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    print(get_response.read().decode())

    get_url = 'http://192.168.1.1/cgi-bin/luci/admin/home'

    get_request = urllib.request.Request(get_url, headers=headers)
    get_response = opener.open(get_request)
    ret = str(get_response.read().decode())
    ret_list = ret.split("\n")
    len(ret_list)
    token=''
    for line in ret_list:
        if('token' in line):
           token_list =  line.split("'")
           token=token_list[1]
    print(token)



    #del route mapping
    add_url = 'http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle'
    values = {'token': token, 'op': 'del', 'srvname': srvname, 'client': client, 'protocol': 'TCP',
              'exPort': exPort, 'inPort': inPort}
    postdata = urllib.parse.urlencode(values).encode()
    request = urllib.request.Request(add_url, postdata, headers)
    try:
        response = opener.open(request)
        print(response.read().decode())
    except urllib.error.URLError as e:
        print(e.reason)

    #add route mapping

    add_url = 'http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle'
    values = {'token':token, 'op': 'add','srvname':srvname,'client':client,'protocol':'TCP','exPort':exPort,'inPort':inPort}
    postdata = urllib.parse.urlencode(values).encode()
    request = urllib.request.Request(add_url, postdata, headers)
    try:
        response = opener.open(request)
        print(response.read().decode())
    except urllib.error.URLError as e:
        print(e.reason)





# See PyCharm help at https://www.jetbrains.com/help/pycharm/

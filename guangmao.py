
import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket

#生成一个类guangmao
class guangmao:
    #初始化
    def __init__(self):
        self.user_agent =  r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36' \
                 r' (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive'}
        self.cookie_filename='cookie.txt'
        self.login_url='http://192.168.1.1/cgi-bin/luci'
        self.openers = None
        self._login()
        
    def _login(self):
        #定义一个登录的数据
        login_data = {'username': 'useradmin', 'psd': '*****'}
        #将数据转换为url编码
        login_data = urllib.parse.urlencode(login_data).encode()
        #定义一个请求
        login_request = urllib.request.Request(self.login_url, login_data, self.headers)
   

        cookie_aff = http.cookiejar.MozillaCookieJar(self.cookie_filename)
        handler = urllib.request.HTTPCookieProcessor(cookie_aff)
        self.openers = urllib.request.build_opener(handler)
        request = urllib.request.Request(self.login_url, login_data, self.headers)
        try:
           response = self.openers.open(request)
        except urllib.error.URLError as e:
           print(e.reason)
        cookie_aff.save(ignore_discard=True, ignore_expires=True)


    def _get_info(self,get_url):
        get_request = urllib.request.Request(get_url, headers=self.headers)
        get_response = self.openers.open(get_request)
        print(get_response.read().decode())
        return ""
    def _crud(self,action,server,client,exPort,inPort):
        return ""

    def allInfo(self):
        return self._get_info("http://192.168.1.1/cgi-bin/luci/admin/allInfo")

    def add_port_bind(self,srvname,client,exPort,inPort):
        return ""    
    def del_port_bind(self,srvname,client,exPort,inPort):
        return ""
    def pmDisplay(self):
        return ""


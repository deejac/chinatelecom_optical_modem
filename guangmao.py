
import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket
import json

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
        self.inports={"remote_desktop":3389,"ftp":21,"ssh":22,"telnet":23,"http":80,"https":443,"mysql":3306,"mssql":1433}
        self.exports={"remote_desktop":3389,"ftp":21,"ssh":16822,"telnet":23,"http":80,"https":443,"mysql":3306,"mssql":1433}
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
        return get_response.read().decode()
    def _crud(self,action,server,client,exPort,inPort):
        return ""

    def allInfo(self):
        return self._get_info("http://192.168.1.1/cgi-bin/luci/admin/allInfo")

    def _load_json_content(self, json_content):
        #加载json数据
        json_data = json.loads(json_content)
        return json_data

    def get_pc_ip(self):
        json_content = self.allInfo()
        json_data = self._load_json_content(json_content)
        pc_key=""
        for key, value in json_data.items():
            if(type(value) == type({})):
                for key1, value1 in value.items():
                    if(value1=="DESKTOP-94N64HN"):
                        pc_key=key
        ip =  json_data[pc_key]["ip"]              
        return ip  

    def get_bind_ip(self):
        json_content = self.pmDisplay()
        json_data = self._load_json_content(json_content)
        bind_key=""
        for key, value in json_data.items():
            if(type(value) == type({})):
                for key1, value1 in value.items():
                    #print(key1,value1)
                    if(value1=="rd"):
                        bind_key=key
        ip=json_data[bind_key]["client"]                             
        return ip   
    
    def update_remote_desktop(self):
        return self.update_port_bind("rd",str(self.exports["remote_desktop"]),str(self.inports["remote_desktop"]))
    
    def update_port_bind(self,srvname,exPort,inPort):
        pc_ip = self.get_pc_ip()
        bind_ip = self.get_bind_ip()
        if pc_ip == bind_ip:
            print("no need to update")
        else:
            client=pc_ip
            self.del_port_bind(srvname,client,exPort,inPort)
            self.add_port_bind(srvname,client,exPort,inPort)
        return ""    

    def add_port_bind(self,srvname,client,exPort,inPort):
        return ""    
    def del_port_bind(self,srvname,client,exPort,inPort):
        return ""
    def pmDisplay(self):
        return self._get_info("http://192.168.1.1/cgi-bin/luci/admin/settings/pmDisplay")


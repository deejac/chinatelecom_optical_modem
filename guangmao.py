
import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket
import json
import smtplib
import urllib
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
from typing import List
#生成一个类guangmao
class guangmao:
    #初始化
    def __init__(self,args: List[str]):
        self.user_agent =  r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36' \
                 r' (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent, 'Connection': 'keep-alive'}
        self.cookie_filename='cookie.txt'
        self.login_url='http://192.168.1.1/cgi-bin/luci'
        self.logout_url='http://192.168.1.1/cgi-bin/luci/admin/logout'
        self.set_url='http://192.168.1.1/cgi-bin/luci/admin/settings/pmSetSingle'
        self.home_url='http://192.168.1.1/cgi-bin/luci/admin/home'
        self.openers = None
        self.inports={"remote_desktop":3389,"ftp":21,"ssh":22,"telnet":23,"http":80,"https":443,"mysql":3306,"mssql":1433}
        self.exports={"remote_desktop":3389,"ftp":21,"ssh":16822,"telnet":23,"http":80,"https":443,"mysql":3306,"mssql":1433}
        self.token=""
        if(len(args)>=6):
          self.from_addr = args[0]
          self.password = args[1]
          self.to_addr =  args[2]
          self.smtp_server = args[3]
          self.title = args[4]
          self.psd = args[5]
        self._login()
        self._get_token()
    @staticmethod
    def sendEmail(from_addr, password, to_addr, smtp_server, title, manual_msg):  # 发送邮件
        def _format_addr(s):
            name, addr = parseaddr(s)
            return formataddr((Header(name, 'utf-8').encode(), addr))

        msg = MIMEText('主人，远程端口的ip变了：' + manual_msg, 'plain', 'utf-8')
        msg['From'] = _format_addr('raspberry pi mode 3<%s>' % from_addr)
        msg['To'] = _format_addr('admin<%s>' % to_addr)
        msg['Subject'] = Header(title, 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()    
    
    def _login(self):
        #定义一个登录的数据
        login_data = {'username': 'useradmin', 'psd': self.psd}
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
           print('login success!')
        except urllib.error.URLError as e:
           print(e.reason)
        cookie_aff.save(ignore_discard=True, ignore_expires=True)

    def _logout(self):
        logout_data = {'token': self.token}
        logout_data = urllib.parse.urlencode(logout_data).encode()
        logout_request = urllib.request.Request(self.logout_url, logout_data, self.headers)
        try:
          logout_response = self.openers.open(logout_request)
          logout_response.read().decode()
          print(logout_response.read().decode(),'logout success')
        except urllib.error.URLError as e:
              print(e.reason)
              self.openers.close()   
        return  logout_response  


    def _get_token(self):
        get_url = self.home_url
        get_request = urllib.request.Request(get_url, headers=self.headers)
        get_response = self.openers.open(get_request)
        ret = str(get_response.read().decode())
        ret_list = ret.split("\n")
        len(ret_list)
        token=''
        for line in ret_list:
         if('token' in line):
           token_list =  line.split("'")
           token=token_list[1]
        self.token=token    
        return token
    
    def _get_info(self,get_url):
        get_request = urllib.request.Request(get_url, headers=self.headers)
        get_response = self.openers.open(get_request)
        return get_response.read().decode()
    def _crud(self,action,srvname,client,exPort,inPort):
        values = {'token':self.token, 'op': action,'srvname':srvname,'client':client,'protocol':'TCP','exPort':exPort,'inPort':inPort}
        postdata = urllib.parse.urlencode(values).encode()
        request = urllib.request.Request(self.set_url, postdata, self.headers)
        ret=0
        try:
          response = self.openers.open(request)
          print(response.read().decode())
        except urllib.error.URLError as e:
          ret=1
          print(e.reason)
        return ret

    def allInfo(self):
        return self._get_info("http://192.168.1.1/cgi-bin/luci/admin/allInfo")

    def _load_json_content(self, json_content):
        #加载json数据
        try:
            json_data = json.loads(json_content)
            return json_data
        except Exception as e:
            print(e)
            return None

    def get_pc_ip(self):
        json_content = self.allInfo()
        json_data = self._load_json_content(json_content)
        if json_data is None:
            print("load allInfo json_data is None")
            return None
        pc_key=""
        for key, value in json_data.items():
            if(type(value) == type({})):
                for key1, value1 in value.items():
                    if(value1=="DESKTOP-94N64HN"):
                        pc_key=key
        if(pc_key==""):
            return None
        ip =  json_data[pc_key]["ip"]              
        return ip  

    def get_bind_ip(self):
        json_content = self.pmDisplay()
        json_data = self._load_json_content(json_content)
        if json_data is None:
            print("load allInfo json_data is None")
            return None
        bind_key=""
        for key, value in json_data.items():
            if(type(value) == type({})):
                for key1, value1 in value.items():
                    #print(key1,value1)
                    if(value1=="rd"):
                        bind_key=key
        if(bind_key==""):
            return None
        ip=json_data[bind_key]["client"]                             
        return ip   
    
    def update_remote_desktop(self):
        ret,msg =  self.update_port_bind("rd", str(self.exports["remote_desktop"]), str(self.inports["remote_desktop"]))
        self._logout()
        return ret,msg

    def update_pi_ssh(self):
        ret,msg =  self.update_port_bind("pi-22", str(self.exports["ssh"]), str(self.inports["ssh"]))
        self._logout()
        return ret,msg

    
    def update_port_bind(self,srvname,exPort,inPort):
        pc_ip = self.get_pc_ip()
        bind_ip = self.get_bind_ip()
        ret = 0
        msg="pc_ip:"+str(pc_ip)+" bind_ip:"+str(bind_ip)
        if pc_ip == None or bind_ip == None:
            print("get pc ip or bind ip error")
            return ret,msg

        if pc_ip == bind_ip:
            print("no need to update")
            ret=2
        else:
            client=pc_ip
            ret = self.del_port_bind(srvname,client,exPort,inPort)
            ret = self.add_port_bind(srvname,client,exPort,inPort)
            self.sendEmail(self.from_addr, self.password, self.to_addr,self.smtp_server,self.title, pc_ip)
            if(ret==0):
                print("update success")
            ret=1
        return ret,msg
    def add_port_bind(self,srvname,client,exPort,inPort):
        self._crud("add",srvname,client,exPort,inPort)
         
    def del_port_bind(self,srvname,client,exPort,inPort):
        self._crud("del",srvname,client,exPort,inPort)
    def pmDisplay(self):
        return self._get_info("http://192.168.1.1/cgi-bin/luci/admin/settings/pmDisplay")





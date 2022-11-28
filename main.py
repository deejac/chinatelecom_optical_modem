import urllib.error, urllib.request, urllib.parse
import http.cookiejar
import socket
from guangmao import guangmao
import sys
#创建基于flask的web应用
from flask import Flask,current_app, render_template, request, redirect, url_for
from gevent import pywsgi
app = Flask(__name__)




@app.route('/')
def index():

    return  "hello world"

@app.route('/update',methods=['GET','POST'])
def update():
    args =  app.config.get("args")
    gm = guangmao(args)
    ret,msg =  gm.update_remote_desktop()
    return "update success ret="+ str(ret)+" msg="+msg

@app.route('/update_pi',methods=['GET','POST'])
def update_pi():
    args =  app.config.get("args")
    #获取flask request中的参数
    srvname = request.args.get('srvname')
    client = request.args.get('client')
    exPort = request.args.get('exPort')
    inPort = request.args.get('inPort')
    gm = guangmao(args)
    ret = 0
    ret =  gm.del_port_bind(srvname,client,exPort,inPort)
    ret =  gm.add_port_bind(srvname,client,exPort,inPort)
    gm._logout()
    return "update success ret="+ str(ret)


@app.route('/allinfo',methods=['GET','POST'])
def allinfo():
    args =  app.config.get("args")
    gm = guangmao(args)
    ret = gm.allInfo()
    gm._logout()
    return ret

@app.route('/pmDisplay',methods=['GET','POST'])
def pmDisplay():
    args =  app.config.get("args")
    gm = guangmao(args)
    ret = gm.pmDisplay()
    gm._logout()
    return ret





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if(sys.argv[7]=="server_on"):
        #启动web应用,并设置端口为5000
        app.config['args'] = sys.argv[1:]
        #app.run(host='0.0.0.0',port=5000)
        server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        server.serve_forever()
    else:
        gm= guangmao(sys.argv[1:])
        gm.update_remote_desktop()

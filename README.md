# chinatelecom_optical_modem
中国电信光猫通过python做端口绑定

电信光猫端口绑定一般需要登录光猫网关，手动添加，当局域网是通过wifi接入，局域网ip总是变化
总是手动更改很麻烦。本代码通过基于cookie登录光猫网关，然后模拟光猫做端口转发的增删。

使用方式：
python main.py  xxx@xxx.com 邮箱密码 xxx@xxx.com smtp.163.com 树莓派远程桌面绑定更改 电信光猫路由器密码 server_on
七个参数
前4个参数是用来自动发送邮件用的，是发件地址，收件地址，发件邮箱的密码，等
第5个参数是邮件标题
第6个参数是电信光猫的登录密码，一般在光猫背面有
第7个参数 server_on 是启动服务。


启动服务后，访问：

http://127.0.0.1:5000/pmDisplay 可以看到路由器的绑定结果

http://127.0.0.1:5000/allinfo   可以看到路由器接入

http://192.168.1.8:5000/update_pi?srvname=flask&client=192.168.1.8&inPort=5000&exPort=5000 可以添加新的绑定记录
其中 client 是需要绑定的内网ip地址
inPort是内网端口
exPort是外网端口

如果有问题，请联系 deejac@qq.com

import unittest
#导入上级目录的guangmao模块
import sys
sys.path.append("..")
from guangmao import guangmao
#创建一个guangmao.py的测试类
class guangmao_test(unittest.TestCase):
    def setUp(self):
        self.gm = guangmao(['deejac@163.com','SUJSZPVUAAVTNPGZ', 'deejac@163.com', 'smtp.163.com', '树莓派远程桌面绑定更改', 'bqfnn'])
    def tearDown(self):
        pass
    def test_allInfo(self):
        self.gm.allInfo()
        print(self.gm.allInfo())
    def test_pmDisplay(self):
        self.gm.pmDisplay()
    def test_get_pc_ip(self):
        self.gm.get_pc_ip()
    def test_get_bind_ip(self):
        self.gm.get_bind_ip()
    def test_update_remote_desktop(self):
        self.gm.update_remote_desktop() 
    def test_login_logout(self):
        self.gm._login()
        self.gm._logout()
#执行测试类
if __name__ == '__main__':
    unittest.main()
    
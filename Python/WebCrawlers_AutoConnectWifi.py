# coding:gbk

import re
import os
import urllib
import urllib2
import time
import subprocess
import types
import socket


class Login:

    def __init__(self):
        self.username = ''
        self.password = ''
        self.ip_pre = '192.168'
        self.overtime = 720
        self.every = 10

    def get_now_time(self):
        return '%s000' % str(int(time.time()))

    def get_current_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def get_ip(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        if self.ip_pre in str(local_ip):
            return str(local_ip)
        ip_lists = socket.gethostbyname_ex(socket.gethostname())
        for ip_list in ip_lists:
            if isinstance(ip_list, list):
                for ip in ip_list:
                    if self.ip_pre in str(ip):
                        return str(ip)
            elif isinstance(ip_list, types.StringType):
                if self.ip_pre in ip_list:
                    return ip_list

    def login(self):
        print '%s 正在尝试认证无线网络' % self.get_current_time()
        ip = self.get_ip()
        data = {
            "username": self.username,
            "password": self.password,
            "serverType": "",
            "isSavePass": "on",
            "Submit1": "",
            "Language": "Chinese",
            "ClientIP": ip,
            "timeoutvalue": 45,
            "heartbeat": 240,
            "fastwebornot": False,
            "StartTime": self.get_now_time(),
            #持续时间，超过这个时间自动掉线，可进行设置
            "shkOvertime": self.overtime,
            "strOSName": "",
            "iAdptIndex": "",
            "strAdptName": "",
            "strAdptStdName": "",
            "strFileEncoding": "",
            "PhysAddr": "",
            "bDHCPEnabled": "",
            "strIPAddrArray": "",
            "strMaskArray": "",
            "strMask": "",
            "iDHCPDelayTime": "",
            "iDHCPTryTimes": "",
            "strOldPrivateIP": ip,
            "strOldPublicIP": ip,
            "strPrivateIP": ip,
            "PublicIP": ip,
            "iIPCONFIG": 0,
            "sHttpPrefix": "http://192.168.8.10",
            "title": "CAMS Portal"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3;WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                          '/38.0.2125.111 Safari/537.36',
            'Host': '192.168.8.10',
            'Origin': 'http://192.168.8.10',
            'Referer': 'http://192.168.8.10/portal/index_default.jsp?Language=Chinese'
        }
        post_data = urllib.urlencode(data)
        login_url = 'http://192.168.8.10/portal/login.jsp?Flag=0'
        try:
            request = urllib2.Request(login_url, post_data, headers)
            response = urllib2.urlopen(request)
            result = response.read().decode('gbk').encode('gbk', 'ignore')
            self.get_login_result(result)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('%s 访问网络出错，服务器网址不存在：%s' % (self.get_current_time(), login_url))
                exit(1)

    def get_login_result(self, result):
        if '用户上线成功' in result:
            print '%s 用户上线成功，在线时长为%s分钟' % (self.get_current_time(), self.overtime/60)
        elif '您已经建立了连接' in result:
            print '%s 您已经建立了连接，无需重复登陆' % self.get_current_time()
        elif '用户不存在' in result:
            print '%s 用户不存在，请检查学号是否正确'% self.get_current_time()
        elif '用户密码错误' in result:
            print '%s 用户密码错误，请检查密码是否正确'% self.get_current_time()
        else:
            print '%s 未知错误，请检查学号密码是否正确' % self.get_current_time()

    def can_connect(self):
        # os.devnull 在不同的系统上null设备的路径，在Windows下为‘nul’，在POSIX下为‘/dev/null’
        fnull = open(os.devnull, 'w')
        # shell=True时，如果args（函数第一参数）是字符串，Popen直接调用系统的Shell来执行args指定的程序，如果args是一个序列，
        # 则args的第一项是定义程序命令字符串，其它项是调用系统Shell时的附加参数。
        result = subprocess.call('ping www.baidu.com', shell=True, stdout=fnull, stderr=fnull)
        fnull.close()
        # result 为 0表示子进程完成成功，否则有错误
        if not result:
            return True
        else:
            return False

    def start(self):
        print '%s 您好，欢迎使用模拟登陆系统' % self.get_current_time()
        while 1:
            now_ip = self.get_ip()
            if not now_ip:
                print '%s 请检查是否正常连接无线网络' % self.get_current_time()
            else:
                print '%s 成功连接了网络，本机IP为%s' % (self.get_current_time(), now_ip)
                self.login()
                while 1:
                    can_connect = self.can_connect()
                    if not can_connect:
                        now_ip = self.get_ip()
                        if not now_ip:
                            print '%s 当前已经掉线，请确保连接上了无线网络' % self.get_current_time()
                        else:
                            print '%s 当前已经掉线，正在尝试重新连接' % self.get_current_time()
                            self.login()
                    else:
                        print '%s 当前网络正常' % self.get_current_time()
                    # Python time sleep() 函数推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间
                    time.sleep(self.every)
            time.sleep(self.every)


def main():
    login = Login()
    login.start()

if __name__ == '__main__':
    main()

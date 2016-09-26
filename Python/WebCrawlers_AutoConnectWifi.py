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
        print '%s ���ڳ�����֤��������' % self.get_current_time()
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
            #����ʱ�䣬�������ʱ���Զ����ߣ��ɽ�������
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
                print('%s �������������������ַ�����ڣ�%s' % (self.get_current_time(), login_url))
                exit(1)

    def get_login_result(self, result):
        if '�û����߳ɹ�' in result:
            print '%s �û����߳ɹ�������ʱ��Ϊ%s����' % (self.get_current_time(), self.overtime/60)
        elif '���Ѿ�����������' in result:
            print '%s ���Ѿ����������ӣ������ظ���½' % self.get_current_time()
        elif '�û�������' in result:
            print '%s �û������ڣ�����ѧ���Ƿ���ȷ'% self.get_current_time()
        elif '�û��������' in result:
            print '%s �û�����������������Ƿ���ȷ'% self.get_current_time()
        else:
            print '%s δ֪��������ѧ�������Ƿ���ȷ' % self.get_current_time()

    def can_connect(self):
        # os.devnull �ڲ�ͬ��ϵͳ��null�豸��·������Windows��Ϊ��nul������POSIX��Ϊ��/dev/null��
        fnull = open(os.devnull, 'w')
        # shell=Trueʱ�����args��������һ���������ַ�����Popenֱ�ӵ���ϵͳ��Shell��ִ��argsָ���ĳ������args��һ�����У�
        # ��args�ĵ�һ���Ƕ�����������ַ������������ǵ���ϵͳShellʱ�ĸ��Ӳ�����
        result = subprocess.call('ping www.baidu.com', shell=True, stdout=fnull, stderr=fnull)
        fnull.close()
        # result Ϊ 0��ʾ�ӽ�����ɳɹ��������д���
        if not result:
            return True
        else:
            return False

    def start(self):
        print '%s ���ã���ӭʹ��ģ���½ϵͳ' % self.get_current_time()
        while 1:
            now_ip = self.get_ip()
            if not now_ip:
                print '%s �����Ƿ�����������������' % self.get_current_time()
            else:
                print '%s �ɹ����������磬����IPΪ%s' % (self.get_current_time(), now_ip)
                self.login()
                while 1:
                    can_connect = self.can_connect()
                    if not can_connect:
                        now_ip = self.get_ip()
                        if not now_ip:
                            print '%s ��ǰ�Ѿ����ߣ���ȷ������������������' % self.get_current_time()
                        else:
                            print '%s ��ǰ�Ѿ����ߣ����ڳ�����������' % self.get_current_time()
                            self.login()
                    else:
                        print '%s ��ǰ��������' % self.get_current_time()
                    # Python time sleep() �����Ƴٵ����̵߳����У���ͨ������secsָ��������ʾ���̹����ʱ��
                    time.sleep(self.every)
            time.sleep(self.every)


def main():
    login = Login()
    login.start()

if __name__ == '__main__':
    main()

# coding:gbk

import re
import string
import urllib
import urllib2
import cookielib


class SDU:

    def __init__(self, login_url, grade_url):
        self.login_url = login_url
        self.grade_url = grade_url
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        # �ύ��ʱ��¼���˺ź�����
        self.post_data = urllib.urlencode(
            {
                'stuid': '',
                'pwd': '',
            }
        )

    def get_page(self):
        try:
            request = urllib2.Request(self.login_url, self.post_data)
            response = self.opener.open(request)
            response_grade = self.opener.open(self.grade_url)
            return response_grade.read().decode('gbk')
        except urllib2.URLError, e:
            print(e.message.strip())
            return None

    def get_grades(self):
        page = self.get_page()
        if not page:
            return None, None
        pattern = re.compile(r'<TR>.*?<p.*?<p.*?<p.*?<p.*?<p.*?>(.*?)</p>.*?<p.*?<p.*?>(.*?)</p>.*?</TR>', re.S)
        items = re.findall(pattern, page)
        credit = [item[0].encode('gbk', 'ignore') for item in items]
        grades = [item[1].encode('gbk', 'ignore') for item in items]
        return credit, grades

    def get_grade(self):
        credit, grades = self.get_grades()
        if not credit and not grades:
            return 'ץȡ�ɼ�ҳ���ѧ�ֺͳɼ�Ϊ %s, %s' % (credit, grades)
        sum = 0.0
        weight = 0.0
        for i in xrange(len(credit)):
            # �ж� �ַ����Ƿ�ֻ�����������
            if grades[i].isdigit():
                # atof�����ַ���ת��Ϊ����������
                # atoi: ���ַ���ת��Ϊ��������
                sum += string.atof(credit[i])*string.atof(grades[i])
                weight += string.atof(credit[i])
        return '��ѧ�ڼ���Ϊ��%s' % sum/weight


def main():
    login_url = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bks_login2.login'
    grade_url = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
    sdu = SDU(login_url, grade_url)
    print sdu.get_grade()

if __name__ == '__main__':
    main()

# coding:gbk
import os

import re
import cookielib
import urllib
import urllib2


class TBMM:

    def __init__(self, base_url):
        self.baseUrl = base_url
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        # ��¼ҳ��ʱ�ύ�����û���������
        self.post_data = urllib.urlencode({
            'TPL_username': 'xxxx',
            'TPL_password': 'XXXX'
        })

    def get_page(self, page_index):
        try:
            url = '%s?page=%s' % (self.baseUrl, str(page_index))
            print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('gbk').encode('gbk', 'ignore')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('�����Ա���ʧ�ܣ�����ԭ��%s' % e.reason)
                return None

    def get_contents(self, page_index):
        page = self.get_page(page_index)
        pattern = re.compile(r'<div class="list-item">.*?<a href="(.*?)".*?>.*?<img src="(.*?)".*?>.*?'
                             r'<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?</em>.*?<span>'
                             r'(.*?)</span>.*?<a href=".*?".*?>', re.S)
        items = re.findall(pattern, page)
        return [[item[0], item[1], item[2], item[3], item[4]] for item in items]

    def get_detail_page(self, info_url):
        try:
            request = urllib2.Request(info_url, self.post_data)
            response = self.opener.open(request)
            return response.read().decode('gbk').encode('gbk', 'ignore')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('������Ů��ʧ�ܣ� ����ԭ��%s' % e.reason)
                return None

    def get_brief(self, page):
        pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        mm_content = re.search(pattern, page)
        return mm_content.group(1).strip()

    def get_all_images(self, page):
        pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        content = re.search(pattern, page)
        pattern_image = re.compile(r'<img.*?src="(.*?)">', re.S)
        images = re.findall(pattern_image, content.group(1))
        return images

    def save_images(self, images, name):
        number = 1
        print('����%s����%s����Ƭ' % (name, len(images)))
        for image_url in images:
            split_path = image_url.split('.')
            fTail = split_path.pop()
            if len(fTail) > 3:
                fTail = 'jpg'
            filename = '%s/%s.%s' % (name, str(number), fTail)
            self.save_image(image_url, filename)
            number += 1

    def save_brief(self, mm_content, name):
        filename = '%s/%s.txt' % (name, name)
        f = open(filename, 'w+')
        print('����͵͵�������ĸ�����ϢΪ%s' % filename)
        f.write(mm_content.encode('utf-8'))

    def save_image(self, image_url, filename):
        u = urllib.urlopen(image_url)
        data = u.read()
        f = open(filename, 'wb')
        f.write(data)
        print('�������ı�������һ��ͼƬΪ%s' % filename)
        f.close()

    def mkdir(self, path):
        path = os.path.join(os.getcwd(), path.strip())
        if not os.path.exists(path):
            print('͵͵�½������ֽ���%s���ļ���' % path)
            os.makedirs(path)
            return True
        else:
            print('��Ϊ%s���ļ����Ѿ������ɹ�' % path)
            return False

    def save_page_info(self, page_index):
        contents = self.get_contents(page_index)
        for item in contents:
            print('-------------------------------------------------------------------')
            print('����һλģ��,���ֽ� %s,���� %s,���� %s' % (item[2], item[3], item[4]))
            print('����͵͵�ر��� %s ����Ϣ' % item[2])
            print('������ط������ĸ��˵�ַ�� http:%s' % item[0])
            detail_url = 'http:%s' % item[0]
            detail_page = self.get_detail_page(detail_url)
            mm_content = self.get_brief(detail_page)
            images = self.get_all_images(detail_page)
            self.mkdir(item[2])
            self.save_brief(mm_content, item[2])
            self.save_images(images, item[2])


def main():
    base_url = 'http://mm.taobao.com/json/request_top_list.htm'
    tbmm = TBMM(base_url)
    tbmm.save_page_info(1)


if __name__ == '__main__':
    main()
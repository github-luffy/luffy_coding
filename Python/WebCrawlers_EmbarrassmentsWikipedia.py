# coding:gbk

import re
import time
import thread
import urllib
import urllib2


class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []    # ��Ŷ��ӵı�����ÿһ��Ԫ����ÿһҳ�Ķ�����
        self.enable = False  # ��ų����Ƿ�������еı���

    def getPage(self, pageIndex):
        """
            ץȡ���°ٿ�������ҳ�����ݡ�
        :param pageIndex:
        :return:
        """
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8').encode('gbk', 'ignore')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('�������°ٿ�ʧ�ܣ�����ԭ��%s' % e.reason)
                return None

    def getPageItems(self, pageIndex):
        """
            ��ȡ���ӷ����ߣ��������ݣ��͵�����������������һ�����С�
        :param pageIndex:
        :return:
        """
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('ҳ�����ʧ�ܡ�����')
            return None
        pattern = re.compile(r'<div class="author.*?">.*?<a.*?<img.*?>.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div'
                             r'.*?>.*?</div>.*?</div>.*?<a.*?>.*?<div.*?content">.*?<span>(.*?)</span>.*?</div>.*?</a>'
                             r'.*?<div.*?>.*?<span.*?><.*?number">(.*?)</i>.*?</span>.*?<span.*?>.*?<span.*?>.*?</span>'
                             r'.*?<a.*?>.*?<i.*?number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR, "\n", item[1])
            pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[3].strip()])
        return pageStories

    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        """
            ÿ��ͨ���ûس�����ӡ���һ������.
        :param pageStories:
        :param page:
        :return:
        """
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            # q�����˳�
            if input == "q":
                self.enable = False
                return
            print('��%sҳ ������:%s ��:%s ����:%s' % (page, story[0], story[2], story[3]))
            print('��������:%s' % story[1])

    def start(self):
        """
            ��ʼ����
        :return:
        """
        print('���ڶ�ȡ���°ٿƣ����س��鿴�¶��ӣ� Q�˳���')
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]  # ɾ����ҳ��ץȡ������
                self.getOneStory(pageStories, nowPage)


def main():
    spider = QSBK()
    spider.start()

if __name__ == '__main__':
    main()


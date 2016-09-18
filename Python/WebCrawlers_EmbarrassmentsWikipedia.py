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
        self.stories = []    # 存放段子的变量，每一个元素是每一页的段子们
        self.enable = False  # 存放程序是否继续运行的变量

    def getPage(self, pageIndex):
        """
            抓取嗅事百科热门网页的内容。
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
                print('连接嗅事百科失败，错误原因：%s' % e.reason)
                return None

    def getPageItems(self, pageIndex):
        """
            获取段子发布者，段子内容，和点赞数；并将其存放在一序列中。
        :param pageIndex:
        :return:
        """
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print('页面加载失败。。。')
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
            每次通过敲回车键打印输出一个段子.
        :param pageStories:
        :param page:
        :return:
        """
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            # q代表退出
            if input == "q":
                self.enable = False
                return
            print('第%s页 发布人:%s 赞:%s 评论:%s' % (page, story[0], story[2], story[3]))
            print('发布内容:%s' % story[1])

    def start(self):
        """
            开始方法
        :return:
        """
        print('正在读取嗅事百科，按回车查看新段子， Q退出：')
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]  # 删除该页已抓取的内容
                self.getOneStory(pageStories, nowPage)


def main():
    spider = QSBK()
    spider.start()

if __name__ == '__main__':
    main()


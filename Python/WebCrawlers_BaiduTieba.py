# coding:gbk

import re
import urllib
import urllib2


class ReplaceTool:

    remove_image = re.compile(r'<img.*?>| {7}|')
    remove_address = re.compile(r'<a.*?>|</a>')
    replace_br = re.compile(r'<br><br>|<br>')
    replace_blank = re.compile(r' +')
    replace_extra_tag = re.compile(r'<.*?>')

    def replace(self, content):
        handled_content = re.sub(self.remove_image, '', content)
        handled_content = re.sub(self.remove_address, '', handled_content)
        handled_content = re.sub(self.replace_br, '\n', handled_content)
        handled_content = re.sub(self.replace_blank, '', handled_content)
        handled_content = re.sub(self.replace_extra_tag, '', handled_content)
        return handled_content.strip()


class BDTB:

    def __init__(self, base_url, see_lz, floor_tag):
        self.baseURL = base_url
        self.seeLZ = '?see_lz=' + str(see_lz)
        self.replaceTool = ReplaceTool()
        self.defaultTitle = '百度贴吧'
        self.file = None
        self.floor = 1
        self.floorTag = floor_tag

    def get_page(self, page_num):
        """
            获取整个页面的内容
        """
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(page_num)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8').encode('gbk', 'ignore')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('连接百度贴吧失败，错误原因：%s' % e.reason)
                return None

    def get_title(self, page):
        """
            获取贴吧标题
        """
        title_pattern = re.compile(r'<h3.*?>(.*?)</h3>', re.S)
        title = re.search(title_pattern, page)
        if title:
            try:
                # group()或者group(0)：匹配正则表达式整体结果
                # group(1):第一个括号匹配部分
                return title.group(1).strip()
            except IndexError, e:
                return 'Error:%s' % e.message.strip()
        else:
            return None

    def get_page_num(self, page):
        page_num_pattern = re.compile(r'<li class="l_reply_num.*?><span.*?>.*?</span>.*?<span class="red">(.*?)</span>'
                                      r'.*?</li>', re.S)
        page_num = re.search(page_num_pattern, page)
        if page_num:
            try:
                return page_num.group(1).strip()
            except IndexError, e:
                return 'Error:%s' % e.message.strip()
        else:
            return None

    def get_page_content(self, page):
        content_pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(content_pattern, page)
        contents = ['\n' + self.replaceTool.replace(item) + '\n' for item in items]
        return contents

    def set_file_title(self, title):
        if not title:
            title = self.defaultTitle
        self.file = open(title + '.txt', 'w')

    def write_content(self, contents):
        for content in contents:
            if self.floorTag == '1':
                floor_line = '\n' + str(self.floor) + ' 楼------------------------------------------------------------' \
                                                      '---------------------------------------\n'
                self.file.write(floor_line)
                self.floor += 1
            self.file.write(content)

    def start(self):
        index_page = self.get_page(1)
        page_num = self.get_page_num(index_page)
        title = self.get_title(index_page)
        self.set_file_title(title)
        if not page_num:
            print('URL已失效，请重试')
            return
        try:
            print('该帖子共有%s页' % str(page_num))
            for i in xrange(1, int(page_num) + 1):
                print('正在写入第%s页内容' % str(i))
                page = self.get_page(i)
                contents = self.get_page_content(page)
                self.write_content(contents)
        except IOError, e:
            print('写入异常，错误原因:%s' % e.message.strip())
        finally:
            self.file.close()
            print('写入任务成功。')


def main():
    print('请输入帖子代号')
    base_url = 'http://tieba.baidu.com/p/' + str(raw_input('http://tieba.baidu.com/p/'))
    see_lz = raw_input('是否只获取楼主发言，是输入1，否输入0\n')
    floor_tag = raw_input('是否写入楼层信息，是输入1，否输入0\n')
    bdtb = BDTB(base_url, see_lz, floor_tag)
    bdtb.start()

if __name__ == '__main__':
    main()

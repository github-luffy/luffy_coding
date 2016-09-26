# coding:gbk

import re
import sys
import time
import urllib
import urllib2


class Iask:

    def __init__(self, base_url, category_url):
        self.base_url = base_url
        self.category_url = category_url
        self.page_index = 1
        self.question_num = 1

    def get_page(self, category_url):
        try:
            url = ''.join([self.base_url, category_url])
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8').encode('gbk', 'ignore')
            return page
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('Error: %s' % e.reason)
                exit(0)

    def get_page_title(self, page):
        title_pattern = re.compile(r'<h3 class="panel-title">(.*?)</h3>', re.S)
        panel_title = re.search(title_pattern, page)
        return panel_title.group(1).strip()

    def get_page_content(self, page):
        question_pattern = re.compile(r'<div class="question-title">.*?<a href="(.*?)".*?>(.*?)</a>.*?<span.*?>(.*?)'
                                      r'</span>.*?<span>(.*?)</span>', re.S)
        items = re.findall(question_pattern, page)
        contents = [[item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip()] for item in items]
        return contents

    def get_page_num(self, page):
        page_num_pattern = re.compile(r'<div class="pages".*?pageCount="(.*?)"', re.S)
        page_num = re.search(page_num_pattern, page)
        return page_num.group(1).strip()

    def get_next_page_url(self, page):
        next_page_url_pattern = re.compile(r'<div class="pages".*?>.*?<span>.*?<a href=".*?" class="cur">.*?</a>.*?'
                                           r'<a href="(.*?)" class="">.*?</a>', re.S)
        next_page_url = re.search(next_page_url_pattern, page)
        return next_page_url.group(1).strip()

    def get_current_time(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def get_current_date(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def create_file(self, panel_title):
        if '/' in panel_title:
            panel_title = panel_title.replace('/', '_')
        filename = '%s.txt' % panel_title
        f_question = open(filename, 'w')
        return f_question

    def get_answers_page(self, html):
        try:
            url = ''.join([self.base_url, html])
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8').encode('gbk', 'ignore')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print('Error:%s' % e.reason)
                exit(0)

    def get_answers(self, page):
        answer_pattern1 = re.compile('<div class="answer_text">.*?<span><pre.*?>(.*?)</pre>', re.S)
        answer_pattern2 = re.compile('<div class="answer_txt">.*?<span><pre.*?>(.*?)</pre>', re.S)
        answer1 = re.findall(answer_pattern1, page)
        answer2 = re.findall(answer_pattern2, page)
        if not answer1 and not answer2:
            return []
        elif answer1 and not answer2:
            return answer1
        elif not answer1 and answer2:
            return answer2
        else:
            answer1 += answer2
            return answer1

    def write_to_file(self, f_question, content):
        answer_page = self.get_answers_page(content[0])
        answers = self.get_answers(answer_page)
        f_question.write('问题 %s------------------------------------------------------------------------\n' %
                         self.question_num)
        f_question.write('问题发布时间为：%s\n' % content[3])
        f_question.write('具体问题为：%s\n' % content[1])
        f_question.write('回答人数为：%s\n' % content[2])
        for answer_index, answer in enumerate(answers):
            f_question.write('回答%s：%s\n' % (answer_index + 1, answer.strip()))
        f_question.write('\n')

    def start(self):
        page = self.get_page(self.category_url)
        panel_title = self.get_page_title(page)
        f_question = self.create_file(panel_title)
        page_num = self.get_page_num(page)
        while 1:
            print('保存的该页内容的网址为：%s' % ''.join([self.base_url, self.category_url]))
            page = self.get_page(self.category_url)
            page_contents = self.get_page_content(page)
            print('%s 总共有%s页的问题,正在保存第%s页问题...\n' % (self.get_current_time(), page_num, self.page_index))
            for content in page_contents:
                self.write_to_file(f_question, content)
                self.question_num += 1

            if self.page_index >= int(page_num) - 1:
                break
            self.category_url = self.get_next_page_url(page)
            self.page_index += 1


def main():
    # 以下两句表示：所有的print语句输出的内容会保存到out.log文件中
    f_handler = open('out.log', 'w')
    sys.stdout = f_handler
    base_url = 'http://iask.sina.com.cn'
    category_url = '/c/866.html'
    iask = Iask(base_url, category_url)
    iask.start()

if __name__ == '__main__':
    main()
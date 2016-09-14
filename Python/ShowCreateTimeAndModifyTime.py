# !/usr/bin/python
# encoding: utf-8

import os
import sys
import time


def main(**kwargs):

    def show_file_created_modified_visited_time():
        t = os.stat(video_path)
        created_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(t.st_ctime))  # ??????
        modified_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(t.st_mtime))
        visited_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(t.st_atime))
        # created_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(os.path.getctime(video_path)))  # ??????
        # modified_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(os.path.getmtime(video_path)))
        # visited_time = time.strftime('%Y年%m月%d日,%H:%M:%S', time.localtime(os.path.getatime(video_path)))
        print('created time : %s' % created_time)
        print('modified time : %s' % modified_time)
        print('visited time : %s' % visited_time)

    dir_path = os.path.join(os.getcwd(), kwargs['using_dir'])
    print("the path of %s dir is '%s'" % (sys.argv[1], dir_path))
    for path, folders, files in os.walk(dir_path):
        mp4_list = [file for file in files if file.endswith('.mp4')]
        print mp4_list
        for (index, video) in enumerate(mp4_list):
            video_path = os.path.join(path, video)
            print((str(index + 1) + ': %s') % video_path)
            show_file_created_modified_visited_time()

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write('Usage:%s original_dir' % sys.argv[0])
        sys.exit(1)
    else:
        print('sys.argv[0] = %s' % sys.argv[0])

    if not os.path.isdir(sys.argv[1]):
        sys.stderr.write('Error: not a directory: %s\n' % sys.argv[1])
        exit(1)

    main(using_dir=sys.argv[1])

# coding:gbk

import os
import time
import datetime
import shutil


def makedir(path):
    try:
        os.makedirs(path)
    except OSError:
        pass


def main(number=None):
    # one pattern:
    today = datetime.date.today().strftime('%Y.%m.%d')
    # second pattern:
    today1 = time.strftime('%Y.%m.%d', time.localtime())

    dir_path = os.path.join(os.getcwd(), root_dir)
    makedir(dir_path)

    print(root_dir + ' is processing: ')
    print(card_disk)
    print('-------------------------------')
    card_disk_path = card_disk + ":\\"
    print('Processing number %s card : %s...' % (str(number), card_disk_path))

    video_dir = today + '接受的卡' + str(number)
    video_dir_path = os.path.join(dir_path, video_dir)
    makedir(video_dir_path)

    try:
        card_disk_things_list = os.listdir(card_disk_path)
    except WindowsError:
        print('Error:not exists: %s' % card_disk_path)
    else:
        if not card_disk_things_list:
            print('The card is empty.')
        else:
            for thing in card_disk_things_list:
                src_path = os.path.join(card_disk_path, thing)
                if os.path.isdir(src_path):
                    new_dir = os.path.join(video_dir_path, thing)
                    try:
                        shutil.copytree(src_path, new_dir)
                    except WindowsError:
                        print('Error:%s has existed' % new_dir)
                elif os.path.isfile(src_path):
                    # if file has existed, it will be overwritten.
                    shutil.copy(src_path, video_dir_path)
            print('Copy : Done')

            for thing in os.listdir(card_disk_path):
                src = os.path.join(card_disk_path, thing)
                if os.path.isfile(src):
                    os.remove(src)
                elif os.path.isdir(src):
                    shutil.rmtree(src, True)
            print('Remove : Done')

if __name__ == '__main__':

    root_dir = 'NJ_1_1_02'
    card_disk = 'W'
    main(number=5)

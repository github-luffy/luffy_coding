# coding:gbk

import os
import time
import collections


def handle_car_day_bootstrap(path):
    with open(path) as fi:
        image_name_list = []
        image_path_list = []
        for line in fi.readlines():
            image_name_in_fi = line.strip().rsplit('\\', 1)[-1]
            image_name_list.append(image_name_in_fi)
            image_path_list.append(line.strip())
        return image_name_list, image_path_list


def make_image_number_dict(path):
    with open(path) as f1:
        image_name_list = []
        image_number_list = []
        for line in f1.readlines():
            if not line:
                return
            image_name_in_f1 = line.strip().split('\t', 1)[0]
            image_numbers_in_f1 = line.strip()
            image_name_list.append(image_name_in_f1)
            image_number_list.append(image_numbers_in_f1)
        return collections.OrderedDict(zip(image_number_list, image_name_list))


def write_to_merge_txt(path, image_number_dict, image_path_dict):
    try:
        with open(path, 'w') as merge_file:
            for image_number, image_name in image_number_dict.iteritems():
                number = image_number.split('\t', 1)[-1]
                try:
                    text_line = ' '.join([image_path_dict[image_name], number])
                    merge_file.write(text_line + '\n')
                except KeyError:
                    print image_name
    except IOError, value:
        print('IOError: [Error 13] Permission denied: %s' % value.filename)
        print('Please make sure %s not open.' % value.filename)


def main():

    start_time = time.time()

    path1 = os.path.join(os.getcwd(), txt1)
    path2 = os.path.join(os.getcwd(), txt2)
    path3 = os.path.join(os.getcwd(), txt3)
    path4 = os.path.join(os.getcwd(), txt4)

    image_number_dict = make_image_number_dict(path1)

    image_name_list1, image_path_list1 = handle_car_day_bootstrap(path2)
    image_name_list2, image_path_list2 = handle_car_day_bootstrap(path3)
    image_path_dict = dict(zip((image_name_list1 + image_name_list2),
                               (image_path_list1 + image_path_list2)))

    write_to_merge_txt(path4, image_number_dict, image_path_dict)
    end_time = time.time()

    print('start time : %s' % start_time)
    print('end time : %s' % end_time)
    print 'run time : %s' % str(end_time - start_time)

if __name__ == '__main__':

    txt1 = '未处理的图片_准备条形图挑漏.txt'

    txt2 = 'car_day_bootstrap_160905_45W1.txt'

    txt3 = 'car_day_bootstrap_160905_45W2.txt'

    txt4 = 'merge.txt'

    main()

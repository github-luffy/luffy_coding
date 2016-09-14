# coding:gbk

import os
import sys
from os.path import join
import cv2.cv as cv


def make_image_points_dic_from_txt():
    with open(join(os.getcwd(), image_points_file)) as read_file:
        for line in read_file.readlines():
            if line == '':
                break
            image_name_path = line.strip().split()[0]
            image_points_list = line.strip().rsplit('\\', -1)[-1].split()
            image_name = image_points_list[0]
            points_list = [[int(image_points_list[i * 2 + 1]), int(image_points_list[i * 2 + 2])]
                           for i in xrange((len(image_points_list) - 1)/2)]
            image_points_dic.setdefault(image_name, points_list)
            image_path_dic.setdefault(image_name, image_name_path)


def make_image_list_from_folder():
    image_li = [image for image in os.listdir(join(os.getcwd(), image_folder))]
    return image_li


def main(*args, **kwargs):
    """
        check points on image weather the position of points is right.
        if the position of points is wrong ,give the right position of points.
    """
    print("kwargs = %s" % kwargs)

    def show_message_on_image(text=None, start_position=None, text_color=None):
        font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1, 1, 0, 1, 8)
        cv.PutText(image, text, start_position, font, text_color)

    def show_points_on_image():
        points_list_temp = image_points_dic[image_name]
        for point_index, point in enumerate(points_list_temp):
            cv.Circle(image, (point[0], point[1]), point_radius, (0, 255, 255), -1, 8, 0)
            show_message_on_image(str(point_index + 1), (point[0] + 1, point[1]), (0, 255, 255))

    def are_points_satisfied():
        input_points_num = len(image_points_dic[image_name])
        if input_points_num % kwargs['point_num'] != 0 and input_points_num != 0:
            error_text = str(kwargs['point_num'])+' points needed,but only '+str(input_points_num)+' points found.'
            error_start_position = (1, int(image.height / 2))
            show_message_on_image(error_text, error_start_position, text_color=(255, 255, 0))
            cv.ShowImage('CheckPoints', image)
            cv.WaitKey(500)
            return False
        else:
            return True

    def check_up(event, x, y, flags, image):

        if event == cv.CV_EVENT_FLAG_LBUTTON:
            # make points on image
            cv.Circle(image, (x, y), point_radius, (0, 255, 255), -1, 8, 0)
            kwargs['point_added'] = [x, y]

        if event == cv.CV_EVENT_FLAG_RBUTTON:
            # change the color of point : yellow -> green
            if not (x == 0 and y == 0):
                for temp_point in image_points_dic[image_name]:
                    if abs(temp_point[0] - x) <= 1 and abs(temp_point[1] - y) <= 1:
                        kwargs['point_removed'] = [temp_point[0], temp_point[1]]
                        cv.Circle(image, (temp_point[0], temp_point[1]), point_radius, (0, 255, 0), -1, 8, 0)
                    else:
                        cv.Circle(image, (temp_point[0], temp_point[1]), point_radius, (0, 255, 255), -1, 8, 0)

        cv.ShowImage('CheckPoints', image)

    image_index = 0
    image_name_list = make_image_list_from_folder()
    has_removed_point = False
    while 0 <= image_index < len(image_name_list):
        image_name = image_name_list[image_index]
        if image_name in image_points_dic.iterkeys():
            # print image_name
            points_on_image = len(image_points_dic[image_name])
            image = cv.LoadImage(join(os.getcwd(), image_folder, image_name))
            show_points_on_image()
            image_num_text = str(image_index + 1) + "/" + str(len(image_name_list))
            num_start_position = (1, int(image.height - 1))
            show_message_on_image(image_num_text, num_start_position, text_color=(255, 255, 0))
            cv.ShowImage('CheckPoints', image)
            cv.SetMouseCallback('CheckPoints', check_up, image)  # check_up : CallBack Function
            response = cv.WaitKey(0)

            if response == 27:   # esc : quit
                if not are_points_satisfied():
                    continue
                is_quit_text = "Are you sure to quit？(y/n)"
                quit_start_position = (1, int(image.height / 2))
                show_message_on_image(is_quit_text, quit_start_position, text_color=(255, 255, 0))
                cv.ShowImage('CheckPoints', image)
                quit_response = cv.WaitKey(0)
                is_quit = False
                while True:
                    if quit_response in list((121, 131161)):
                        is_quit = True
                        break
                    elif quit_response in list((110, 131150)):
                        break
                    else:
                        quit_response = cv.WaitKey(0)
                if is_quit:
                    break

            if response == 103:  # g : next image
                if not are_points_satisfied():
                    continue
                image_index += 1
                if image_index >= len(image_name_list):
                    image_index = len(image_name_list) - 1

            if response == 114:  # r: last image
                if not are_points_satisfied():
                    continue
                image_index -= 1
                if image_index < 0:
                    image_index = 0

            if response == 32:
                if kwargs['point_added']:
                    if has_removed_point:
                        image_points_dic[image_name].insert(remove_index, kwargs['point_added'])
                    else:
                        image_points_dic[image_name].insert(points_on_image + 1, kwargs['point_added'])
                    show_points_on_image()
                    kwargs['point_added'] = None
                    has_removed_point = False

            if response == 100:
                if kwargs['point_removed'] in image_points_dic[image_name]:
                    remove_index = image_points_dic[image_name].index(kwargs['point_removed'])
                    print('remove index: %s' % remove_index)
                    print('The number of %s is removed,the point is %s.' %
                          (str(remove_index + 1), (kwargs['point_removed'][0], kwargs['point_removed'][1])))
                    image_points_dic[image_name].pop(remove_index)
                    has_removed_point = True

    with open(join(os.getcwd(), image_points_file_checked), 'w') as write_file:
        for final_image_name in image_name_list:
            temp_list = []
            if final_image_name in image_points_dic.iterkeys():
                temp_list.append(image_path_dic[final_image_name])
                for final_point in image_points_dic[final_image_name]:
                    temp_list.append(str(final_point[0]))
                    temp_list.append(str(final_point[1]))
                write_file.write(' '.join(temp_list) + '\n')

if __name__ == '__main__':

    image_points_file = sys.argv[1]
    
    image_folder = sys.argv[2]

    if len(sys.argv) != 3:
        sys.stderr.write('Usage:%s ImageFolder ImagePointsFile\n' % (sys.argv[0], image_folder, image_points_file))
        sys.exit(1)

    if not os.path.isfile(join(os.getcwd(), image_points_file)):
        sys.stderr.write('%s is not a file.\n' % image_points_file)
        sys.exit(1)

    if not os.path.isdir(join(os.getcwd(), image_folder)):
        sys.stderr.write('%s is not a directory.\n' % image_folder)
        sys.exit(1)

    image_points_file_checked = image_points_file.rsplit('.', 1)[0] + '_checked' + '.' + \
                                image_points_file.rsplit('.', 1)[-1]
    point_radius = 2

    image_points_dic = {}

    image_path_dic = {}

    make_image_points_dic_from_txt()

    main(point_added=None, point_removed=None, magnification=1, point_num=4)




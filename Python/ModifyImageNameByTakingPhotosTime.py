# coding=gbk

import os
import random
import stat                 # ����ļ���ϵͳ״̬��Ϣ
import time
import exifread             # ���ͼƬexif��Ϣ

'''
    ��������ʱ�佫��Ƭ�ļ����޸�Ϊһ�¸�ʽ��
    2014-03-15_091230.jpg(%Y-%m-%d_%H%M%S)
'''
MY_DATE_FORMAT = '%Y-%m-%d_%H%M%S'                           # format��ʽ���ַ���
SUFFIX_FILTER = ['.jpg', '.png', '.mpg', '.mp4', '.thm', '.bmp', '.jpeg', '.avi', '.mov']
DELETE_FILES = ['thumbs.db', 'sample.dat']


# �ж��Ƿ��Ѿ��Ǹ�ʽ�������ļ���
def isFormatedFileName(filename):
    try:
        filename_no_path = os.path.basename(filename)           # ȥ��Ŀ¼·���������ļ���
        f, e = os.path.splitext(filename_no_path)               # �����ļ�ǰ�����ֺ���չ��
        time.strptime(f, MY_DATE_FORMAT)                        # ��f����ָ����ʽ����Ϊʱ��Ԫ��
        return True
    except ValueError:
        return False


# �����ļ���չ�����ж��Ƿ�����Ҫ������ļ�����
def isTargetedFileType(filename):
    filename_no_path = os.path.basename(filename)
    f, e = os.path.splitext(filename_no_path)
    if e.lower() in SUFFIX_FILTER:
        return True
    else:
        return False


# �ж��Ƿ���ָ��Ҫɾ�����ļ�
def isDeleteFile(filename):
    filename_no_path = os.path.basename(filename)
    if filename_no_path.lower() in DELETE_FILES:
        return True
    else:
        return False


# ������Ƭ������ʱ�������µ��ļ����������ȡ��������ʱ�䣬��ʹ���ļ��Ĵ���ʱ�䣩
def generateNewFileName(filename):
    " ��ȡ��Ƭ������ʱ��"
    try:
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
        else:
            raise "[%s] is not a file!\n" % filename
    except:
        raise Exception("[%s] doesn't open!\n" % filename)
    data = exifread.process_file(fd)   # ��ȡexif��Ϣ���ֵ�
    if data:
        try:
            t = data['EXIF DateTimeOriginal']  # ��ȡ����ʱ�䣬��ʽΪyyyy:mm:dd H:M:S
            dateStr = str(t).replace(':', '_')[:10] + '_' + str(t)[11:].replace(':', '')
        except:
            pass
    else:
        fileState = os.stat(filename)       # ��ȡ�ļ�״̬��Ϣ
        dateStr = time.strftime('%Y_%m_%d_%H%M%S', time.localtime(fileState[-2]))
    dirname = os.path.dirname(filename)
    filename_no_path = os.path.basename(filename)
    f, e = os.path.splitext(filename_no_path)
    new_file_name = os.path.join(dirname, dateStr + e).lower()
    return new_file_name


# ����ָ��Ŀ¼�Լ���Ŀ¼���������������ļ����и�������ɾ��
def scandir(startdir):
    for obj in os.listdir(startdir):
        obj = os.path.join(startdir, obj)
        if os.path.isfile(obj):
            if isFormatedFileName(obj) is False and isTargetedFileType(obj):
                new_file_name = generateNewFileName(obj)
                new_file_name = isSameFileName(startdir, new_file_name)
                print "rename [%s] => [%s]" % (obj, new_file_name)
                # os.rename(os.path.join(startdir, obj), os.path.join(startdir, new_file_name))
                os.rename(obj, new_file_name)
            elif isDeleteFile(obj):
                print "delete [%s]:" % obj
                os.remove(obj)
            else:
                pass
        if os.path.isdir(obj):
            scandir(obj)


# �ж�ͬĿ¼�µ��ļ��Ƿ�ͬ��
# ����һȱ�㣺���ļ�����ͬ�����ļ��ܶ࣬��ô���������Ҳ�����ͬ������
def isSameFileName(samedir, new_file_name):
    dirname = os.path.dirname(new_file_name)
    new_file_name_no_path = os.path.basename(new_file_name)
    if new_file_name_no_path in os.listdir(samedir):
        f, e = os.path.splitext(new_file_name_no_path)
        return os.path.join(dirname, f + '_' + str(random.randint(0, 1000)) + e)
    else:
        return new_file_name

if __name__ == '__main__':
    path = os.getcwd()
    startdir = os.path.join(path, 'folder')
    scandir(startdir)
    # scandir("E:\\python\\Study\\8�·�\\folder")

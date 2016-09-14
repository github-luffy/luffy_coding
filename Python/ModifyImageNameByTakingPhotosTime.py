# coding=gbk

import os
import random
import stat                 # 相关文件的系统状态信息
import time
import exifread             # 获得图片exif信息

'''
    根据拍照时间将照片文件名修改为一下格式：
    2014-03-15_091230.jpg(%Y-%m-%d_%H%M%S)
'''
MY_DATE_FORMAT = '%Y-%m-%d_%H%M%S'                           # format格式化字符串
SUFFIX_FILTER = ['.jpg', '.png', '.mpg', '.mp4', '.thm', '.bmp', '.jpeg', '.avi', '.mov']
DELETE_FILES = ['thumbs.db', 'sample.dat']


# 判断是否已经是格式化过的文件名
def isFormatedFileName(filename):
    try:
        filename_no_path = os.path.basename(filename)           # 去掉目录路径，返回文件名
        f, e = os.path.splitext(filename_no_path)               # 返回文件前面名字和扩展名
        time.strptime(f, MY_DATE_FORMAT)                        # 将f按照指定格式解析为时间元组
        return True
    except ValueError:
        return False


# 根据文件扩展名，判断是否是需要处理的文件类型
def isTargetedFileType(filename):
    filename_no_path = os.path.basename(filename)
    f, e = os.path.splitext(filename_no_path)
    if e.lower() in SUFFIX_FILTER:
        return True
    else:
        return False


# 判断是否是指定要删除的文件
def isDeleteFile(filename):
    filename_no_path = os.path.basename(filename)
    if filename_no_path.lower() in DELETE_FILES:
        return True
    else:
        return False


# 根据照片的拍照时间生成新的文件名（如果获取不到拍照时间，则使用文件的创建时间）
def generateNewFileName(filename):
    " 获取照片的拍摄时间"
    try:
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
        else:
            raise "[%s] is not a file!\n" % filename
    except:
        raise Exception("[%s] doesn't open!\n" % filename)
    data = exifread.process_file(fd)   # 获取exif信息的字典
    if data:
        try:
            t = data['EXIF DateTimeOriginal']  # 获取拍摄时间，格式为yyyy:mm:dd H:M:S
            dateStr = str(t).replace(':', '_')[:10] + '_' + str(t)[11:].replace(':', '')
        except:
            pass
    else:
        fileState = os.stat(filename)       # 获取文件状态信息
        dateStr = time.strftime('%Y_%m_%d_%H%M%S', time.localtime(fileState[-2]))
    dirname = os.path.dirname(filename)
    filename_no_path = os.path.basename(filename)
    f, e = os.path.splitext(filename_no_path)
    new_file_name = os.path.join(dirname, dateStr + e).lower()
    return new_file_name


# 遍历指定目录以及子目录，对满足条件的文件进行改名或者删除
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


# 判断同目录下的文件是否同名
# 存在一缺点：当文件名中同名的文件很多，那么随机的名字也会造成同名现象
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
    # scandir("E:\\python\\Study\\8月份\\folder")

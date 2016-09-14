#!/usr/bin/python
# encode: utf-8

import os
import re
import sys
import shutil
import subprocess
from os.path import join


#  copy videos from original video folder
def copy_video(file_path):

    new_folder_path = join(os.getcwd(), new_folder)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    shutil.copy(file_path, new_folder_path)

    has_copied_no_rename = rename_video(file_path, new_folder_path)

    if not has_copied_no_rename:
        unpack_video(new_folder_path)


# use subprocess : calculate hash values
def calculate_hash_value(file_path):

    output = subprocess.check_output(['/usr/bin/sha1sum', file_path]) 
    return re.search(r'([0-9a-f]+)', output).group(1)


# rename video names
def rename_video(file_path, new_folder_path):

    if '/' in original_video_folder:
        original_video_folder_no_slash = original_video_folder.replace('/', '')
    else:
        original_video_folder_no_slash = original_video_folder

    file_name = os.path.basename(file_path)
    name_no_extension = file_name.rsplit('.', 1)[0]
    hash_values = calculate_hash_value(file_path)
    new_file_name = '_'.join([original_video_folder_no_slash, name_no_extension, hash_values[:8]]) + '.' + file_name.rsplit('.', 1)[-1]

    if new_file_name in os.listdir(new_folder_path):
        os.remove(join(new_folder_path, file_name))
        sys.stderr.write('%s has copied already.\n' % file_name)
        return True

    os.rename(join(new_folder_path, file_name), join(new_folder_path, new_file_name))
    return False


def process_file(new_file_path):

    if not new_file_path.endswith('.mp4'):
        return

    print('Processing file : %s' % new_file_path)
    new_file_name = os.path.basename(new_file_path)
    rel_path = new_file_name.rsplit('.', 1)[0]
    image_folder_path = join(os.path.dirname(new_file_path).rsplit('/', 1)[0], images_dir)
    image_dir = os.path.join(image_folder_path, rel_path + '_images')

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    command = [UnpackVideo, '-P', str(period), new_file_path, image_dir]
    proc = subprocess.Popen(command)
    proc.communicate()


def process_dir(directory):
    print('Processing directory : %s' % directory)

    for entry in os.listdir(directory):
        entry_path = join(directory, entry)

        if os.path.isfile(entry_path):
            process_file(entry_path)

        elif os.path.isdir(entry_path):
            process_dir(entry_path)


# port : unpack videos from new video folder
def unpack_video(new_folder_path):
    process_dir(new_folder_path)


def main():
    """
        new video folder : copy and rename videos from original video folder;
        new image folder : extract images between period(a integer) frames from videos in new video folder.
    """

    for path, folders, files in os.walk(join(os.getcwd(), original_video_folder)):
        for file in files:
            if file.rsplit('.', 1)[-1] in video_types:
                file_path = join(path, file)
                print('original_video_path : %s' % file_path)
                copy_video(file_path)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s original_video_folder\n' % sys.argv[0])
        exit(1)

    original_video_folder = sys.argv[1]

    # take a image at every 150 frames
    period = 150

    new_folder = 'copy_videos_from_' + original_video_folder
    images_dir = 'extract_images_in_150_frames_from_videos_in_' + original_video_folder
    video_types = ['mp4', 'MP4', 'avi', 'AVI', 'MOV', 'mov', 'asf', 'ASF']

    UnpackVideo = '/opt/unpack_video/unpack_video'   # usage: resolute images
    main()

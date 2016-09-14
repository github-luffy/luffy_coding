# coding:gbk

import os
from PIL import Image, ImageFilter

# The execScript'path
exec_script_path = os.getcwd()

# The folder stores unprocessed images
original_folder = 'folder'

# The folder stores processed images
processed_images_folder = "processed_images_folder"

# The types of image
image_types = ['jpg', 'jpeg', 'bmp', 'gif', 'png']


def main(magnification=1, is_save=False):

    def is_image_type(expanded_name):
        if expanded_name in image_types:
            return True
        else:
            return False

    def process_image(file, file_path):
        expanded_name = file.rsplit('.', 1)[-1]
        if is_image_type(expanded_name):
            image = Image.open(file_path)
            new_image_height = int(image.size[0] * magnification)
            new_image_width = int(image.size[1] * magnification)
            new_image = image.resize((new_image_width, new_image_height)).filter(ImageFilter.DETAIL)
            processed_images_folder_path = os.path.join(exec_script_path, processed_images_folder)
            if not os.path.exists(processed_images_folder_path):
                os.makedirs(processed_images_folder_path)
            if is_save:
                new_image_path = os.path.join(processed_images_folder_path, file)
                new_image.save(new_image_path)

    original_folder_path = os.path.join(exec_script_path, original_folder)
    if not os.path.exists(original_folder_path):
        print "In %s ,%s doesn't exist!" % (original_folder_path, original_folder)
    elif os.path.isdir(original_folder_path):
        for path, folders, files in os.walk(original_folder_path):
            for file in files:
                file_path = os.path.join(path, file)
                process_image(file, file_path=file_path)
        print "Processed Images are saved in %s successfully!" % processed_images_folder
    else:
        print "In %s ,%s is a file!" % (original_folder_path, original_folder)

if __name__ == '__main__':
    print "--------------------------" \
          "---------------------------" \
          "-------------"
    main(magnification=0.5, is_save=True)
    print "--------------------------" \
          "---------------------------" \
          "-------------"
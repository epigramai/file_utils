import cv2
import os
from os_wrapper import list_subfolders, list_images

def batch_resize_images(base_folder_path, with_subfolders, subfolder_branch=''):
    subfolder_path = os.path.join(base_folder_path, subfolder_branch)
    small_subfolder_path = os.path.join(base_folder_path, 'small', subfolder_branch)
    if not os.path.isdir(small_subfolder_path):
        os.mkdir(small_subfolder_path)
    for img_name in list_images(subfolder_path):
        img = cv2.imread(os.path.join(subfolder_path, img_name), 0)
        img = cv2.resize(img, (700, 1000))
        cv2.imwrite(os.path.join(small_subfolder_path, img_name), img)
    if with_subfolders:
        for subsubfolder_name in list_subfolders(subfolder_path):
            # avoid infinite recursion
            if subsubfolder_name != 'small':
                batch_resize_images(base_folder_path, with_subfolders, os.path.join(subfolder_branch, subsubfolder_name))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Categorise images into subfolders')
    parser.add_argument('folder_path', help='The location of the image files')
    parser.add_argument('--with_subfolders', dest='with_subfolders', action='store_true', help='Include subfolders')
    args = parser.parse_args()
    batch_resize_images(args.folder_path, args.with_subfolders)
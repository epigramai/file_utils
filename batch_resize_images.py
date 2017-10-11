import cv2
import os
from itertools import product

from file_utils.cv_wrapper import resize
from file_utils.os_wrapper import list_subfolders, list_images


DEFAULT_QUALITY = 100


def batch_resize_images(base_folder_path, with_subfolders, lengths, qualities, folder_branch=''):
    folder_path = os.path.join(base_folder_path, folder_branch)
    # depth first to avoid infinite recursion
    if with_subfolders:
        for subsubfolder_name in list_subfolders(folder_path):
            batch_resize_images(base_folder_path, with_subfolders, lengths, qualities, os.path.join(folder_branch, subsubfolder_name))
    #heights = {1920, 3000}
    #qualities = {20, 40, 60, 80, 100}
    for length, quality in product(lengths, qualities):
        subfolder_path = os.path.join(base_folder_path, '{}_{}'.format(str(length), str(quality)), folder_branch)
        os.makedirs(subfolder_path, exist_ok=True)
    for img_name in list_images(folder_path):
        img = cv2.imread(os.path.join(folder_path, img_name))
        for length, quality in product(lengths, qualities):
            img_path = os.path.join(base_folder_path, '{}_{}'.format(str(length), str(quality)), folder_branch, img_name)
            cv2.imwrite(img_path, resize(img, length), (cv2.IMWRITE_JPEG_QUALITY, quality))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Categorise images into subfolders')
    parser.add_argument('folder_path', help='The location of the image files')
    parser.add_argument('--with_subfolders', dest='with_subfolders', action='store_true', help='Include subfolders')
    parser.add_argument('--lengths', dest='lengths', type=int, nargs='*', default=[None], help='Lengths to resize to')
    parser.add_argument('--qualities', dest='qualities', type=int, nargs='*', default=[DEFAULT_QUALITY], help='jpg qualities to save as')
    args = parser.parse_args()
    batch_resize_images(args.folder_path, args.with_subfolders, args.lengths, args.qualities)
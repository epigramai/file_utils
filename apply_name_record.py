import argparse
import cv2
import json
import os

from file_utils.os_wrapper import list_images, list_image_branches
from file_utils.py_wrapper import aggregate_keys, aggregate_values, rstrip

JPG_QUALITY = 100


def replace_image_names_with_numbers(name_record_path, folder_path, suffix, with_subfolders, inverse_record):
    image_branches = list_image_branches(folder_path) if with_subfolders else list_images(folder_path)
    with open(name_record_path) as f:
        name_record = json.load(f)
    
    if inverse_record:
        name_record = aggregate_keys(name_record, value_wrapper=lambda x: os.path.splitext(x)[0])
    else:
        name_record = aggregate_values(name_record, key_wrapper=lambda x: os.path.splitext(x)[0])

    for image_branch in image_branches:
        subfolder_branch, old_filename = os.path.split(image_branch)
        old_name, ext = os.path.splitext(old_filename)
        old_name = rstrip(old_name, suffix)
        if not old_name in name_record:
            print('WARNING: {} not in name record, skipping'.format(old_name))
            continue
        new_filenames = name_record[old_name]
        if len(new_filenames) >= 2:
            print('WARNING: {} not unique in name record, skipping'.format(old_name))
            continue
        new_filename, = new_filenames
        new_filename = suffix.join(os.path.splitext(new_filename))
        new_filepath = os.path.join(folder_path, subfolder_branch, new_filename)
        if os.path.isfile(new_filepath):
            print('WARNING: {} already exists, skipping'.format(new_filepath))
            continue
        old_filepath = os.path.join(folder_path, image_branch)
        if ext.lower() not in {'.jpg', '.jpeg'}:
            img = cv2.imread(old_filepath)
            cv2.imwrite(new_filepath, img, (cv2.IMWRITE_JPEG_QUALITY, JPG_QUALITY))
            os.remove(old_filepath)
        else:
            os.rename(old_filepath, new_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply name record')
    parser.add_argument('name_record_path', help='The location of the name record')
    parser.add_argument('folder_path', help='The location of the image files')
    parser.add_argument('--suffix', dest='suffix', default='', help='Suffix to strip and add again')
    parser.add_argument('--with_subfolders', dest='with_subfolders', action='store_true', help='Prepend folder name')
    parser.add_argument('--inverse_record', dest='inverse_record', action='store_true', help='Inverse the name record')
    args = parser.parse_args()
    replace_image_names_with_numbers(args.name_record_path, args.folder_path, args.suffix, args.with_subfolders, args.inverse_record)

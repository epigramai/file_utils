import cv2
import json
import os

from file_utils.os_wrapper import list_images, list_image_branches
from file_utils.py_wrapper import full_outer_compose


JPG_QUALITY = 100


def replace_image_names_with_numbers(folder_path, prepend_folder_name, with_subfolders):
    
    image_branches = sorted(list_image_branches(folder_path) if with_subfolders else list_images(folder_path), key=lambda x: os.path.split(x)[1])
    folder_name = os.path.split(os.path.split(folder_path)[0])[1]
    name_record = {}
    
    for i, image_branch in enumerate(image_branches):
        subfolder_branch, old_filename = os.path.split(image_branch)
        new_filename = (folder_name + '_' if prepend_folder_name else '') + str(i) + '.jpg'
        old_name, ext = os.path.splitext(old_filename)
        if ext.lower() not in {'.jpg', '.jpeg'}:
            img = cv2.imread(os.path.join(folder_path, image_branch))
            cv2.imwrite(os.path.join(folder_path, subfolder_branch, new_filename), img, (cv2.IMWRITE_JPEG_QUALITY, JPG_QUALITY))
            os.remove(os.path.join(folder_path, image_branch))
        else:
            os.rename(os.path.join(folder_path, image_branch), os.path.join(folder_path, subfolder_branch, new_filename))
        name_record[new_filename] = old_filename
    
    name_record_filename = 'name_record.json'
    if os.path.isfile(os.path.join(folder_path, name_record_filename)):
        with open(os.path.join(folder_path, name_record_filename)) as f:
            old_name_record = json.load(f)
    else:
        old_name_record = None
        
    new_name_record = full_outer_compose(old_name_record, name_record)
    with open(os.path.join(folder_path, name_record_filename), 'w') as f:
        json.dump(new_name_record, f, indent=4, separators=(',', ': '))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Rename all images to 0...n-1')
    parser.add_argument('folder_path', help='The location of the image files')
    parser.add_argument('--prepend_folder_name', dest='prepend_folder_name', action='store_true', help='Prepend folder name')
    parser.add_argument('--with_subfolders', dest='with_subfolders', action='store_true', help='Prepend folder name')
    args = parser.parse_args()
    replace_image_names_with_numbers(args.folder_path, args.prepend_folder_name, args.with_subfolders)
    
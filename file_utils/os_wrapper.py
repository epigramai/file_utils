import os


def list_images(folder_path):
    return [img_name for img_name in os.listdir(folder_path) if os.path.splitext(img_name)[1] in ['.jpg', '.JPG', '.png']]


def list_image_branches(folder_path):
    return [os.path.join(branch, img_name) for branch in list_subfolder_branches(folder_path) for img_name in list_images(os.path.join(folder_path, branch))]


def list_subfolders(folder_path):
    return [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]


def list_subfolder_branches(folder_path, branch=''):
    return sum([list_subfolder_branches(folder_path, os.path.join(branch, subfolder)) for subfolder in list_subfolders(os.path.join(folder_path, branch))], [branch])

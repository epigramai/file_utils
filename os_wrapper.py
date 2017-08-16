import os


def list_images(folder_path):
    return [img_name for img_name in os.listdir(folder_path) if os.path.splitext(img_name)[1] in ['.jpg', '.JPG', '.png']]


def list_subfolders(folder_path):
    return [subfolder for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]
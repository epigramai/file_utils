import cv2


def resize_if_necessary(img):
    height, width = img.shape[:2]
    min_height = 200
    max_height = 800
    if height < min_height or height > max_height:
        new_height = max(min(height, max_height), min_height)
        ratio = new_height/height
        return cv2.resize(img, (int(ratio*width), new_height))
    else:
        return img
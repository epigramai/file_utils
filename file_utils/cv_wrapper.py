import cv2


def resize(img, length):
    if not length:
        return img
    h, w = img.shape[:2]
    new_height, new_width = (length, int((length/h)*w)) if h > w else (int((length/w)*h), length)
    return cv2.resize(img, (new_width, new_height))


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
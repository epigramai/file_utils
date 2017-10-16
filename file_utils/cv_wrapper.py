import cv2


def resize(img, length):
    if not length:
        return img
    h, w = img.shape[:2]
    new_height, new_width = (length, int((length/h)*w)) if h > w else (int((length/w)*h), length)
    return cv2.resize(img, (new_width, new_height))


def resize_into_bounds(img, min_length, max_length):
    height, width = img.shape[:2]
    length = max(height, width)
    if length < min_length or length > max_length:
        new_length = max(min(length, max_length), min_length)
        return resize(img, new_length)
    else:
        return img

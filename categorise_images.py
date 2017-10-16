import os
from abc import ABC

import cv2

from file_utils.cv_wrapper import resize_into_bounds
from file_utils.os_wrapper import list_subfolders, list_images


VALID_CHAR_VALS = (list(range(48, 58))  # 0-9
                           + list(range(97, 123))  # a-z
                           + [229]  # å
                           + [230]  # æ
                           + [248]  # ø
                           )


class Image_classifier(ABC):
    
    def __init__(self):
        self.categorised = None
        self.folder_path = None
        self.i_c = None
        self.i_u = None
        self.show_uncategorised = None
        self.total_c = None
        self.total_u = None
        self.uncategorised = None
        
    @classmethod
    def from_path(cls, folder_path):
        classifier = cls()
        classifier.folder_path = folder_path
        
        classifier.uncategorised = list_images(folder_path)
        classifier.categorised = [os.path.join(subfolder, img_path) for subfolder in list_subfolders(folder_path) for img_path in
                       list_images(os.path.join(folder_path, subfolder))]
        classifier.total_u = len(classifier.uncategorised)
        classifier.total_c = len(classifier.categorised)
        classifier.i_u = classifier.i_c = 0
        classifier.show_uncategorised = classifier.total_u > 0
        
        return classifier

    def categorise_images(self) -> None:
        while (True):
            self.i = self.i_u if self.show_uncategorised else self.i_c
            total = self.total_u if self.show_uncategorised else self.total_c
            img_names = self.uncategorised if self.show_uncategorised else self.categorised
            img_name = img_names[self.i]
            img = cv2.imread(os.path.join(self.folder_path, img_name))
            if img is None:
                print('Cannot load image ' + img_name + ', moving to subfolder /-1')
                self.move_image(img_name, '-1')
                continue
            label = str(self.i + 1) + '/' + str(total) + (
            ': ' + os.path.split(img_name)[0] if not self.show_uncategorised else '')
            cv2.imshow(label, resize_into_bounds(img, 200, 800))
            input = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if input == 81:  # left arrow key
                if self.show_uncategorised:
                    self.i_u = (self.i_u - 1) % self.total_u
                else:
                    self.i_c = (self.i_c - 1) % self.total_c
                continue
            if input == 83:  # right arrow key
                if self.show_uncategorised:
                    self.i_u = (self.i_u + 1) % self.total_u
                else:
                    self.i_c = (self.i_c + 1) % self.total_c
                continue
            if input == 82:  # up arrow key
                if self.total_c > 0:
                    self.show_uncategorised = False
                continue
            if input == 84:  # down arrow key
                if self.total_u > 0:
                    self.show_uncategorised = True
                continue
            if input == 8:  # backspace key
                if not self.show_uncategorised:
                    new_img_name = os.path.split(img_name)[1]
                    os.rename(os.path.join(self.folder_path, img_name), os.path.join(self.folder_path, new_img_name))
                    self.categorised.pop(self.i)
                    self.uncategorised.insert(self.i_u, new_img_name)
                    self.total_c -= 1
                    self.total_u += 1
                    self.i_u += 1
                    if self.total_c > 0:
                        self.i_c = self.i_c % self.total_c
                    else:
                        self.show_uncategorised = True
                continue

            if input not in VALID_CHAR_VALS:  # 27 is value of esc key
                break
            self.move_image(img_name, chr(input))
        return
    
    def move_image(self, img_name, subfolder_name):
        subfolder_path = os.path.join(self.folder_path, subfolder_name)
        if not os.path.isdir(subfolder_path):
            os.mkdir(subfolder_path)
        new_img_name = os.path.join(subfolder_name, os.path.split(img_name)[1])
        os.rename(os.path.join(self.folder_path, img_name), os.path.join(self.folder_path, new_img_name))
        if self.show_uncategorised:
            self.uncategorised.pop(self.i)
            self.categorised.append(new_img_name)
            self.total_u -= 1
            self.total_c += 1
            self.i_c = self.total_c - 1
            if self.total_u > 0:
                self.i_u = self.i_u % self.total_u
            else:
                self.show_uncategorised = False
        else:
            self.categorised[self.i] = new_img_name
            self.i_c = (self.i_c + 1) % self.total_c

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Categorise images into subfolders')
    parser.add_argument('folder_path', help='The location of the image files')
    args = parser.parse_args()
    #categorise_images(args.folder_path)
    classifier = Image_classifier.from_path(args.folder_path)
    classifier.categorise_images()
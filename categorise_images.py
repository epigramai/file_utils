import os
from abc import ABC

import cv2

from file_utils.cv_wrapper import resize_if_necessary
from file_utils.os_wrapper import list_subfolders, list_images


def categorise_images(folder_path) -> None:
    valid_char_vals = (list(range(48,58)) #0-9
                       + list(range(97,123)) #a-z
                       + [229] #å
                       + [230] #æ
                       + [248] #ø
                       )
    uncategorised = list_images(folder_path)
    categorised = [os.path.join(subfolder, img_path) for subfolder in list_subfolders(folder_path) for img_path in list_images(os.path.join(folder_path, subfolder))]
    total_u = len(uncategorised)
    total_c = len(categorised)
    i_u = i_c = 0
    show_uncategorised = total_u > 0
    while(True):
        i = i_u if show_uncategorised else i_c
        total = total_u if show_uncategorised else total_c
        img_names = uncategorised if show_uncategorised else categorised
        img_name = img_names[i]
        img = cv2.imread(os.path.join(folder_path, img_name))
        if img is None:
            print('Cannot load image ' + img_name)
            return
        label = str(i + 1) + '/' + str(total) + (': ' + os.path.split(img_name)[0] if not show_uncategorised else '')
        cv2.imshow(label, resize_if_necessary(img))
        input = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if input == 81: # left arrow key
            if show_uncategorised:
                i_u = (i_u - 1) % total_u
            else:
                i_c = (i_c - 1) % total_c
            continue
        if input == 83: # right arrow key
            if show_uncategorised:
                i_u = (i_u + 1) % total_u
            else:
                i_c = (i_c + 1) % total_c
            continue
        if input == 82: # up arrow key
            if total_c > 0:
                show_uncategorised = False
            continue
        if input == 84: # down arrow key
            if total_u > 0:
                show_uncategorised = True
            continue
        if input == 8: # backspace key
            if not show_uncategorised:
                new_img_name = os.path.split(img_name)[1]
                os.rename(os.path.join(folder_path, img_name), os.path.join(folder_path, new_img_name))
                categorised.pop(i)
                uncategorised.insert(i_u, new_img_name)
                total_c -= 1
                total_u += 1
                i_u += 1
                if total_c > 0:
                    i_c = i_c % total_c
                else:
                    show_uncategorised = True
            continue

        if input not in valid_char_vals: # 27 is value of esc key
            break
        subfolder_path = os.path.join(folder_path, chr(input))
        if not os.path.isdir(subfolder_path):
            os.mkdir(subfolder_path)
        new_img_name = os.path.join(chr(input), os.path.split(img_name)[1])
        os.rename(os.path.join(folder_path, img_name), os.path.join(folder_path, new_img_name))
        if show_uncategorised:
            uncategorised.pop(i)
            categorised.append(new_img_name)
            total_u -= 1
            total_c += 1
            i_c = total_c - 1
            if total_u > 0:
                i_u = i_u % total_u
            else:
                show_uncategorised = False
        else:
            categorised[i] = new_img_name
            i_c = (i_c + 1) % total_c
    return

VALID_CHAR_VALS = (list(range(48, 58))  # 0-9
                           + list(range(97, 123))  # a-z
                           + [229]  # å
                           + [230]  # æ
                           + [248]  # ø
                           )


class Image_classifier(ABC):
    
    def __init__(self):
        pass
    
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
            cv2.imshow(label, resize_if_necessary(img))
            input = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if input == 81:  # left arrow key
                if self.show_uncategorised:
                    i_u = (i_u - 1) % self.total_u
                else:
                    i_c = (i_c - 1) % self.total_c
                continue
            if input == 83:  # right arrow key
                if self.show_uncategorised:
                    i_u = (i_u + 1) % self.total_u
                else:
                    i_c = (i_c + 1) % self.total_c
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
                    i_u += 1
                    if self.total_c > 0:
                        i_c = i_c % self.total_c
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
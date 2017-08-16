import cv2
import os
from cv_wrapper import resize_if_necessary
from os_wrapper import list_subfolders, list_images


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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Categorise images into subfolders')
    parser.add_argument('folder_path', help='The location of the image files')
    args = parser.parse_args()
    categorise_images(args.folder_path)
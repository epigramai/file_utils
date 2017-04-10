import cv2
import os


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


def categorise_images(folder_path) -> None:
    valid_char_vals = (list(range(48,58)) #0-9
                       + list(range(97,123)) #a-z
                       + [229] #å
                       + [230] #æ
                       + [248] #ø
                       )
    uncategorised = [img_name for img_name in os.listdir(folder_path) if os.path.splitext(img_name)[1] in ['.jpg', '.JPG', '.png']]
    categorised = []
    total_u = len(uncategorised)
    total_c = 0
    i_u = i_c = 0
    show_uncategorised = True
    while(True):
        i = i_u if show_uncategorised else i_c
        total = total_u if show_uncategorised else total_c
        img_names = uncategorised if show_uncategorised else categorised
        img_name = img_names[i]
        print(img_name)
        img = cv2.imread(os.path.join(folder_path, img_name))
        # TODO: find a way to display uncategorised/categorised and current category
        cv2.imshow(str(i + 1) + '/' + str(total), resize_if_necessary(img))
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
                i_c = i_c % total_c
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
            i_u = i_u % total_u
            i_c = total_c - 1
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
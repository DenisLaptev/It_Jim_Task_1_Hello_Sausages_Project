import numpy as np
from cv2 import imread
from os import walk

import cv2


def create_pictures_dict_list(folder_with_pictures_path):
    pictures_dict_list = []
    for root, dirs, files in walk(folder_with_pictures_path):
        for _file in files:
            picture_dict = {}

            # file
            filename = _file

            # image
            path_to_file = folder_with_pictures_path + '\\' + str(_file)
            image = imread(path_to_file)

            img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 100, 255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)

            # image_sizes
            rows_number = mask_inv.shape[0]
            cols_number = mask_inv.shape[1]

            # sausage_sizes
            left_x = cols_number // 2
            top_y = rows_number // 2

            right_x = cols_number // 2
            bottom_y = rows_number // 2

            for row in range(1, rows_number):
                for col in range(1, cols_number):
                    px = mask_inv[row, col]
                    #print(px)
                    if px == 0:
                        if left_x > col:
                            left_x = col

                        if right_x < col:
                            right_x = col

                        if top_y > row:
                            top_y = row

                        if bottom_y < row:
                            bottom_y = row

            cv2.rectangle(image, (left_x, top_y), (right_x, bottom_y), (0, 0, 255), 1)

            cv2.imshow('image', image)
            cv2.imshow('mask_inv', mask_inv)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            left = bottom_y - top_y
            right = bottom_y - top_y
            top = right_x - left_x
            bottom = right_x - left_x
            picture_sizes_list = [left, right, top, bottom]

            picture_dict['file'] = filename
            picture_dict['coords'] = picture_sizes_list
            picture_dict['img'] = image
            pictures_dict_list.append(picture_dict)

    return pictures_dict_list


def main():
    folder_with_pictures_path = r'..\resources\sausages'
    pictures_dict_list = create_pictures_dict_list(folder_with_pictures_path)
    print(pictures_dict_list)


if __name__ == '__main__':
    main()

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
            image = imread(path_to_file, cv2.IMREAD_GRAYSCALE)
            # image = imread(path_to_file, cv2.IMREAD_COLOR)

            # image_sizes
            rows_number = image.shape[0]
            cols_number = image.shape[1]

            # sausage_sizes
            left_x = cols_number // 2
            top_y = rows_number // 2

            right_x = cols_number // 2
            bottom_y = rows_number // 2

            border_px_list = []
            for row in range(1, rows_number):
                for col in range(1, cols_number):

                    px11 = image[row, col]
                    px01 = image[row - 1, col]
                    px10 = image[row, col - 1]

                    condition1 = abs(int(px11) - int(px01)) >= 22
                    condition2 = abs(int(px11) - int(px01)) <= 130

                    condition3 = abs(int(px11) - int(px10)) >= 22
                    condition4 = abs(int(px11) - int(px10)) <= 130

                    if (condition1 and condition2) or (condition3 and condition4):
                        border_px_list.append(px11)
                        # print('px(', str(row), ',', str(col), ')=', px11)
                        #cv2.circle(image, (col, row), 1, (0, 0, 255), -1)

                        if left_x > col:
                            left_x = col

                        if right_x < col:
                            right_x = col

                        if top_y > row:
                            top_y = row

                        if bottom_y < row:
                            bottom_y = row

            cv2.rectangle(image, (left_x, top_y), (right_x, bottom_y), (0, 255, 0), 2)

            cv2.imshow('image', image)
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

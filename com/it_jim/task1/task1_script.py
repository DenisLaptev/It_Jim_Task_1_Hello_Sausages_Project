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
            # print(filename)

            # image
            path_to_file = folder_with_pictures_path + '\\' + str(_file)
            image = imread(path_to_file, cv2.IMREAD_GRAYSCALE)
            # image = imread(path_to_file, cv2.IMREAD_COLOR)

            # image_sizes
            rows_number = image.shape[0]
            cols_number = image.shape[1]

            left_x = cols_number // 2
            top_y = rows_number // 2

            right_x = cols_number // 2
            bottom_y = rows_number // 2

            left_color = image[top_y, left_x]
            top_color = image[top_y, left_x]

            right_color = image[bottom_y, right_x]
            bottom_color = image[bottom_y, right_x]

            white_px_list = []
            for row in range(rows_number):
                for col in range(cols_number):
                    px = image[row, col]
                    # print(px)
                    if 255 - px <= 1:
                        white_px_list.append(px)
                        # print('px(', str(row), ',', str(col), ')=', px)
                        cv2.circle(image, (col, row), 5, (0, 0, 255), -1)

                        if left_x > col and (px >= left_color):
                            left_x = col
                            left_color = px

                        if right_x < col and (px >= right_color):
                            right_x = col
                            right_color = px

                        if top_y > row and (px >= top_color):
                            top_y = row
                            top_color = px

                        if bottom_y < row and (px >= bottom_color):
                            bottom_y = row
                            bottom_color = px

            # print('len(white_px_list)=', len(white_px_list))
            if len(white_px_list) == 0:
                left_x = 0
                top_y = 0
                right_x = cols_number
                bottom_y = rows_number
                # print('empty')
            cv2.rectangle(image, (left_x, top_y), (right_x, bottom_y), (0, 255, 0), 2)

            cv2.imshow('image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # print('---------------------------------')

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
    folder_with_pictures_path = r'.\sausages'
    pictures_dict_list = create_pictures_dict_list(folder_with_pictures_path)
    print(pictures_dict_list)


if __name__ == '__main__':
    main()

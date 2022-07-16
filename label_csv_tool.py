# @Time    : 2022/7/16 9:56
# @Author  : Dai Yalun
# @File    : csv_renewal_test.py
# csv write renewal

import csv

def csv_item_search(csv_path, name_search):
    csv_read = csv.reader(open(csv_path, 'r'))

    csv_list = []
    for row in csv_read:
        csv_list.append(row)

    new_item_imfor = []
    for i in range(len(csv_list)):
        if name_search == csv_list[i][0]:
            # print(csv_list[i])
            new_item_imfor.append(csv_list[i])
    return new_item_imfor

def csv_stylized_item_add(stylized_filename, stylized_imfor, csv_path):
    csv_file = open(csv_path, 'a')
    for i in range(len(stylized_imfor)):
        [_name, x_min, y_min, x_max, y_max, label] = stylized_imfor[i]
        stylized_imfor_test = stylized_filename + "," + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + "," + label
        print(stylized_imfor_test)
        csv_file.write(
            stylized_filename + "," + str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max) + "," + label + "\n")

    csv_file.close()

content_name  = '5.jpg'
stylized_name = '5-stylized-03.jpg'
csv_path = 'csv_labels.csv'

stylized_imfor = csv_item_search(csv_path, content_name)
csv_stylized_item_add(stylized_name, stylized_imfor, csv_path)



# -*- coding: utf-8 -*-
# create by yihui 11:15 20/9/10.
import codecs
import csv


def save_csv(file_name, rows):
    with open(file_name, 'w+', newline='') as csv_file:
        csv_file.write(codecs.BOM_UTF8.decode())
        writer = csv.writer(csv_file)
        for line in rows:
            writer.writerow(line)

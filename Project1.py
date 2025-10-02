# Name: Zora Tucker
# Student ID: 28071696
# Email: zrtucker@umich.edu
# Worked Alone
# GenAI Use:

import csv

# Part 2
# A list of the variables in the dataset (or in other words, the names of each column)
def read_crop_yield_headers():
    with open("/Users/zoratucker/Downloads/SI 201/fall25-project1-zorarjt/crop_yield.csv") as csv_file:
        csv_read=csv.reader(csv_file, delimiter=',')
        header = next(csv_read)
        return header
print(read_crop_yield_headers())

# sample entry (row) in the dataset
def read_crop_yield_entry():
    with open("/Users/zoratucker/Downloads/SI 201/fall25-project1-zorarjt/crop_yield.csv") as csv_file:
        csv_read=csv.reader(csv_file, delimiter=',')
        next(csv_read)
        entry = next(csv_read)
        return entry
print(read_crop_yield_entry())

# number of rows in the dataset
def read_crop_yield_num_rows():
    with open("/Users/zoratucker/Downloads/SI 201/fall25-project1-zorarjt/crop_yield.csv") as csv_file:
        csv_read=csv.reader(csv_file, delimiter=',')
        next(csv_read)
        for num_rows, row in enumerate(csv_read):
            num_rows += 1 
        return num_rows
print(read_crop_yield_num_rows())
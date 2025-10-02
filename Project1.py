import csv

# Part 2
# A list of the variables in the dataset (or in other words, the names of each column)
def read_crop_yield_headers():
    with open("/Users/zoratucker/Downloads/SI 201/fall25-project1-zorarjt/crop_yield.csv") as csv_file:
        csv_read=csv.reader(csv_file, delimiter=',')
        header = next(csv_read)
        return header
print(read_crop_yield_headers())
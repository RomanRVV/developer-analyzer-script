import csv
import argparse
from tabulate import tabulate
from pprint import pprint


needed_fields = {'name', 'performance'}

paths = ['test_file/employees1.csv', 'test_file/employees2.csv']


data = []
for path in paths:
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

        # for row in reader:
        #     data.append({key: value for key, value in row.items() if key in needed_fields})


        # data = [
        #     {key: value for key, value in row.items() if key in needed_fields}
        #     for row in reader
        # ]
        #

# print(tabulate(data, headers='keys'))
pprint(data)

import csv
from utility.config import MID_CAP_FILE_NAME_CSV, MID_CAP_FILE

fields = []
rows = []

with open(MID_CAP_FILE_NAME_CSV, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row[1])
pickle_write(MID_CAP_FILE, rows[1:])

"""
with open(LARGE_CAP_FILE_NAME_CSV, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row[1])
pickle_write(LARGE_CAP_FILE, rows[1:])
"""


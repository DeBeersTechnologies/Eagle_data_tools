import csv
import os

data_file = open(r'X:\Hong\Stats\Sone status list.csv')
data_dict = csv.DictReader(data_file, delimiter=",")

rem_Counts = [0, 0, 0, 0, 0, 0]
Counts = [0, 0, 0, 0, 0, 0]
start_Counts = [0, 0, 0, 0, 0, 0]
lines = 0

print data_dict.fieldnames

for data_line in data_dict:
    barcode = int(data_line[' Barcode'])
    AP_grade = data_line['Known grade']
    Used = data_line[' Used']
    Too_dirty = data_line[' Empty Folder']
    No_clusters = data_line[' No Cluster']
    failed = data_line[' Failed To Load']
    print AP_grade

    lines += 1

    if No_clusters == ' Yes' and AP_grade == 'VS1' and Used == ' No':
        rem_Counts[2] += 1
    elif No_clusters == ' Yes' and AP_grade == 'VS2' and Used == ' No':
        rem_Counts[3] += 1
    elif No_clusters == ' Yes' and AP_grade == 'SI1' and Used == ' No':
        rem_Counts[4] += 1
    elif No_clusters == ' Yes' and AP_grade == 'SI2' and Used == ' No':
        rem_Counts[5] += 1
    elif No_clusters == ' Yes' and AP_grade == 'VVS1' and Used == ' No':
        rem_Counts[0] += 1
    elif No_clusters == ' Yes' and AP_grade == 'VVS2' and Used == ' No':
        rem_Counts[1] += 1

    if AP_grade == 'VS1' and Too_dirty == ' Yes':
        Counts[2] += 1
    elif AP_grade == 'VS2' and Too_dirty == ' Yes':
        Counts[3] += 1
    elif AP_grade == 'SI1' and Too_dirty == ' Yes':
        Counts[4] += 1
    elif AP_grade == 'SI2' and Too_dirty == ' Yes':
        Counts[5] += 1
    elif AP_grade == 'VVS1' and Too_dirty == ' Yes':
        Counts[0] += 1
    elif AP_grade == 'VVS2' and Too_dirty == ' Yes':
        Counts[1] += 1

    if AP_grade == 'VS1':
        start_Counts[2] += 1
    elif AP_grade == 'VS2':
        start_Counts[3] += 1
    elif AP_grade == 'SI1':
        start_Counts[4] += 1
    elif AP_grade == 'SI2':
        start_Counts[5] += 1
    elif AP_grade == 'VVS1':
        start_Counts[0] += 1
    elif AP_grade == 'VVS2':
        start_Counts[1] += 1

print str(lines) + ' Stones in total'
print rem_Counts,
print 'Stone take out of  classifier for being empty'
print Counts,
print ' taken out for being too dirty'
print start_Counts,
print ' In each category to start with'

data_file.close

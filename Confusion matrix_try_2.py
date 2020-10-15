import csv
import os

hongfile = open('Classifier_Results_5446_samples.csv')  # classsifier generated from Eagle
hongdata = csv.DictReader(hongfile, dialect='excel')
FMfile = open('Allgradesmay.csv')  # Database queried
# FMdata = csv.DictReader(FMfile)


########################################################
### for each classifier record get barcode and grade ###
### look up Q1 and Q2 grades and assign to q1dict &  ###
### q2dict (rows eagle, columns Qn)                  ###
########################################################

FMbarcode = ""
Gradelookup = {'IF': 0, 'VVS1': 1, 'VVS2': 2, 'VS1': 3, 'VS2': 4, 'SI1': 5, 'SI2': 6,
               'I1': 7, 'KM': 8}
# print Gradelookup.keys()

Q1Q2 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Name': 'Q1 vs Q2'}
EQ1 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Name': 'Eagle vs Q1'}
EQ2 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Name': 'Eagle vs Q2'}
ESpot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
         'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
         'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
         'Name': 'Eagle vs Spot'}

# get barcode and eagle(assigned)grade from hongdata
for row in hongdata:
    barcode = int(row[' barcode'])
    print barcode,
    eaglegrade = row[' assigned grade'].strip()
    eaglegraden = Gradelookup[eaglegrade]
    # print eaglegrade

    # look for barcode in FM gradedata
    # get Q1, Q2 and Spot grades, turn into numbers

    FMdata = csv.DictReader(FMfile)

    for row in FMdata:
        FMbarcode = int(row['Barcode '])
        print FMbarcode
        if FMbarcode == barcode:
            print "#", FMbarcode
            Q1grade = row[' Q1 ']
            Q2grade = row[' Q2 ']
            Spotgrade = row['Spot ']
            Q1n = Gradelookup[Q1grade]
            Q2n = Gradelookup[Q2grade]
            Spotn = Gradelookup[Spotgrade]
            # print Q1n,Q2n
            # print Q1grade,Q2grade

            # reset Dictionary
            FMfile.close()
            FMdata = {}
            break

            # update confusion matrix dictionaries

    Q1Q2[Q1grade][Q2n] += 1
    EQ1[eaglegrade][Q1n] += 1
    EQ2[eaglegrade][Q2n] += 1
    ESpot[eaglegrade][Spotn] += 1


##Print it all out##

def printmatrix(mat):
    print

    print mat['Name']
    print '\tIF\tVVS1\tVVS2\tVS1\tVS2\tSI1\tSI2\tI1'
    print 'IF',
    for i in range(0, 8):
        print mat['IF'][i],
    print
    print 'VVS1',
    for i in range(0, 8):
        print mat['VVS1'][i],
    print
    print 'VVS2',
    for i in range(0, 8):
        print mat['VVS2'][i],
    print
    print 'VS1',
    for i in range(0, 8):
        print mat['VS1'][i],
    print
    print 'VS2',
    for i in range(0, 8):
        print mat['VS2'][i],
    print
    print 'SI1',
    for i in range(0, 8):
        print mat['SI1'][i],
    print
    print 'SI2',
    for i in range(0, 8):
        print mat['SI2'][i],
    print
    print 'I1',
    for i in range(0, 8):
        print mat['I1'][i],
    print
    print


def savematrix(mat):
    matrixfile = mat['Name'] + '.csv'
    b = ''
    while b != 'y' and b != 'n':
        a = raw_input('Save ' + matrixfile + '? Y/N ')
        b = a.lower()
    if b == 'y':

        outfile = open(matrixfile, 'w')

        outfile.write('\tIF\tVVS1\tVVS2\tVS1\tVS2\tSI1\tSI2\tI1')
        outfile.write('IF'),
        for i in range(0, 8):
            outfile.write(mat['IF'][i], )
        outfile.write('\n')
        outfile.write('VVS1', )
        for i in range(0, 8):
            outfile.write(mat['VVS1'][i], )
        outfile.write('\n')
        outfile.write('VVS2', )
        for i in range(0, 8):
            outfile.write(mat['VVS2'][i], )
        outfile.write('\n')
        outfile.write('VS1', )
        for i in range(0, 8):
            outfile.write(mat['VS1'][i], )
        outfile.write('\n')
        outfile.write('VS2', )
        for i in range(0, 8):
            outfile.write(mat['VS2'][i], )
        outfile.write('\n')
        outfile.write('SI1', )
        for i in range(0, 8):
            outfile.write(mat['SI1'][i], )
        outfile.write('\n')
        outfile.write('SI2', )
        for i in range(0, 8):
            outfile.write(mat['SI2'][i], )
        outfile.write('\n')
        outfile.write('I1', )
        for i in range(0, 8):
            outfile.write(mat['I1'][i], )
        outfile.write('\n')
        outfile.close


printmatrix(Q1Q2)
printmatrix(EQ1)
printmatrix(EQ2)
printmatrix(ESpot)
savematrix(Q1Q2)
savematrix(EQ1)
savematrix(EQ2)

FMfile.close()
hongfile.close()

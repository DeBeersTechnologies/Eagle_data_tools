import csv
import os
import sys
import pyodbc

barcodefile = open(
    r'F:\Eagle processing\Eagle results Antwerp post classifier\Results files\Eagle14Complete.csv')  # Output of SC script
# remove extra first column
barcodedata = csv.DictReader(barcodefile, delimiter=",")
print barcodedata.fieldnames

# ***********************************************************************************************
# ****** For each barcode in the barcode file (stones which have been through Eagle), query*******
# ****** the data base for Q1, Q2, Q3 Spot and Eagle and construct confusion matrices ************
# ************************************************************************************************


Gradelookup = {'IF': 0, 'VVS1': 1, 'VVS2': 2, 'VS1': 3, 'VS2': 4, 'SI1': 5, 'SI2': 6,
               'I1': 7, 'I2': 8, 'I3': 9, 'Referral': 10, 'Error': 11}

# print Gradelookup.keys()

Q1Q3 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'Name': 'Q1 vs Q2/3'}
EQ1 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Name': 'Eagle vs Q1'}
EQ3 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       'Name': 'Eagle vs Q2/3'}
ESpot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         'Name': 'Eagle vs Spot'}
Q1Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Name': 'Q1 vs Spot'}
Q2Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'I2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I3': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Name': 'Q2/3 vs Spot'}

# Get Barcode
missingcount = 0

conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
cur = conn.cursor()
stonecount = 0

for data_line in barcodedata:
    # print row
    barcode = int(data_line['StoneNumber '])
    print barcode

    Q1grade, Q1sub, Q2grade, Q2sub, Q3grade, Q3sub, Q3Fgrade, Q3Fsub, Sptgrade, Sptsub, eaglegrade = "", "", "", "", \
                                                                                                     "", "", "", "", \
                                                                                                     "", "", ""
    eaglegrade = data_line[' Grade']
    if eaglegrade == "":
        eaglegrade = "Error"
    elif eaglegrade[0] == "#":
        eaglegrade = "Error"

    #    eaglegrade = data_line[' assigned grade'].strip()
    #    hong_known = data_line['Known grade']
    #    eaglegraden = Gradelookup[eaglegrade]

    querystring = "GetClarityGradingDetails " + str(barcode)
    stonecount += 1
    print stonecount
    cur.execute(querystring)
    rows = cur.fetchall()

    for row in rows:
        if row and row.MarkingProcess[0:3] != "Col":
            # print row.MarkingProcess, row.Quality, row.QualitySubGrade
            Grader = row.MarkingProcess
            Quality = row.Quality
            SubGrade = row.QualitySubGrade
            if Grader == "Quality One":
                if Quality != None:
                    Q1grade = Quality
                    Q1sub = SubGrade
            elif Grader == "Quality Two":
                if Quality != None:
                    Q2grade = Quality
                    Q2sub = SubGrade
            elif Grader == "Quality Three":
                if Quality != None:
                    Q3grade = Quality
                    Q3sub = SubGrade
            elif Grader == "Quality Three Final":
                if Quality != None:
                    Q3Fgrade = Quality
                    Q3Fsub = SubGrade
            elif Grader == "Spot Check":
                if Quality != None:
                    Sptgrade = Quality
                    Sptsub = SubGrade
                    # elif Grader == "Clarity Machine":
                    #     if Quality != None and Quality != "NA":
                    #         eaglegrade = Quality
                    #         #if eaglegrade == "SI1":
                    #           #  sys.exit("Found an SI1!")
                    #         eaglegraden = Gradelookup[eaglegrade]

    print Q1grade, Q2grade, Q3grade, Q3Fgrade, Sptgrade, eaglegrade

    if (Q1grade != '' or Q2grade != '' or Q3grade != '') and Sptgrade != '' and eaglegrade != '' \
            and Q1grade != 'KM' and Sptgrade != 'KM' and (Q1grade != 'FL' and Q2grade != 'FL' and Q3grade != 'FL'):
        Q1n = Gradelookup[Q1grade]
        #    Q2n = Gradelookup[Q2grade]
        if Q3grade != '' and Q3grade != 'FL':
            Q3n = Gradelookup[Q3grade]
        elif Q2grade != '' and Q2grade != 'FL':
            Q3n = Gradelookup[Q2grade]
        Spotn = Gradelookup[Sptgrade]

        Q1Q3[Q1grade][Q3n] += 1
        EQ1[eaglegrade][Q1n] += 1
        EQ3[eaglegrade][Q3n] += 1
        ESpot[eaglegrade][Spotn] += 1
        Q1Spot[Q1grade][Spotn] += 1
        if Q3grade != '' and Q3grade != 'FL':
            Q2Spot[Q3grade][Spotn] += 1
        else:  # if Q2grade == '':
            Q2Spot[Q2grade][Spotn] += 1

############
# Print it all out
############
print str(missingcount) + ' barcode missing from data'


def printmatrix(mat):
    print

    print mat['Name']
    print '\tIF\tVVS1\tVVS2\tVS1\tVS2\tSI1\tSI2\tI1\tI2\tI3'

    print 'IF',
    for i in range(0, 10):
        print mat['IF'][i],
    print
    print 'VVS1',
    for i in range(0, 10):
        print mat['VVS1'][i],
    print
    print 'VVS2',
    for i in range(0, 10):
        print mat['VVS2'][i],
    print
    print 'VS1',
    for i in range(0, 10):
        print mat['VS1'][i],
    print
    print 'VS2',
    for i in range(0, 10):
        print mat['VS2'][i],
    print
    print 'SI1',
    for i in range(0, 10):
        print mat['SI1'][i],
    print
    print 'SI2',
    for i in range(0, 10):
        print mat['SI2'][i],
    print
    print 'I1',
    for i in range(0, 10):
        print mat['I1'][i],
    print
    print 'I2',
    for i in range(0, 10):
        print mat['I2'][i],
    print
    print 'I3',
    for i in range(0, 10):
        print mat['I3'][i],
    print
    print 'Referral',
    for i in range(0, 10):
        print mat['Referral'][i],
    print
    print 'Error',
    for i in range(0, 10):
        print mat['Error'][i],
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


printmatrix(Q1Q3)
printmatrix(EQ1)
printmatrix(EQ3)
printmatrix(ESpot)
printmatrix(Q1Spot)
printmatrix(Q2Spot)

# savematrix(Q1Q3)
# savematrix(EQ1)
# savematrix(EQ3)
# savematrix(ESpot)
# savematrix(Q1Spot)
# savematrix(Q2Spot)

barcodefile.close()
cur.close()
del cur

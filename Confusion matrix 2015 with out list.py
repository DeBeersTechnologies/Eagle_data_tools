import csv
import os
import pyodbc

hongfile = open(r'F:\Eagle processing\Stone grading results.csv')  # classsifier generated from Eagle
hongdata = csv.DictReader(hongfile, delimiter=",")

output_file = open(r'F:\Eagle processing\output.csv', 'wb')
outwriter = csv.writer(output_file)
outwriter.writerow(['Barcode', "Eaglegrade", "Spotgrade"])

##FMfile = open('Allgradesmay.csv','rb')  #Database queried
##FMdata = csv.DictReader(FMfile)


print hongdata.fieldnames
##print FMdata.fieldnames

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
Q1Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Name': 'Q1 vs Spot'}
Q2Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0], 'KM': [0, 0, 0, 0, 0, 0, 0, 0, 0],
          'Name': 'Q2 vs Spot'}

# get barcode and eagle(assigned)grade from hongdata
missingcount = 0
for data_line in hongdata:
    # print row
    barcode = int(data_line[' barcode'])
    eaglegrade = data_line[' assigned grade'].strip()
    hong_known = data_line['Known grade']
    eaglegraden = Gradelookup[eaglegrade]

    # print eaglegraden,

    # look for barcode in FM gradedata
    # get Q1, Q2 and Spot grades, turn into numbers

    #    barcodepresent = 1

    ##    for fmrow in FMdata:
    ##        FMbarcode = int(fmrow['Barcode '])
    ##        #print FMbarcode
    ##        if FMbarcode == barcode:
    ##            barcodepresent = 1
    ##            print "#", # FMbarcode, barcode
    ##            Q1grade = fmrow[' Q1 ']
    ##            Q2grade = fmrow[' Q2 ']
    ##            Spotgrade = fmrow['Spot ']
    ##            Q1n = Gradelookup[Q1grade]
    ##            Q2n = Gradelookup[Q2grade]
    ##            Spotn = Gradelookup[Spotgrade]
    ##
    ##            #print Q1n,Q2n
    ##            #print Q1grade,Q2grade
    ##            # reset Dictionary
    ##            FMfile.seek(0)
    ##            #FMdata.__init__(FMfile)
    ##            FMdata.next()
    ##            break

    Q1grade, Q1sub, Q2grade, Q2sub, Q3grade, Q3sub, Q3Fgrade, Q3Fsub, Sptgrade, Sptsub = "", "", "", "", "", "", \
                                                                                         "", "", "", ""
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()
    querystring = "GetClarityGradingDetails " + str(barcode)
    # print querystring
    print '\b#',
    cur.execute(querystring)
    rows = cur.fetchall()

    for row in rows:
        if row and row.MarkingProcess[0:3] != "Col":
            # print row.MarkingProcess, row.Quality, row.QualitySubGrade
            Grader = row.MarkingProcess
            Quality = row.Quality
            SubGrade = row.QualitySubGrade
            if Grader == "Quality One":
                Q1grade = Quality
                Q1sub = SubGrade
            elif Grader == "Quality Two":
                Q2grade = Quality
                Q2sub = SubGrade
            elif Grader == "Quality Three":
                Q3grade = Quality
                Q3sub = SubGrade
            elif Grader == "Quality Three Final":
                Q3Fgrade = Quality
                Q3Fsub = SubGrade
            elif Grader == "Spot Check":
                Sptgrade = Quality
                Sptsub = SubGrade

                #          update confusion matrix dictionaries
    Q1n = Gradelookup[Q1grade]
    Q2n = Gradelookup[Q2grade]
    Spotn = Gradelookup[Sptgrade]

    # print Sptgrade, hong_known
    if Sptgrade != hong_known:
        print "**********************yikes********************************"

    # if barcodepresent==1:

    Q1Q2[Q1grade][Q2n] += 1
    EQ1[eaglegrade][Q1n] += 1
    EQ2[eaglegrade][Q2n] += 1
    ESpot[eaglegrade][Spotn] += 1
    Q1Spot[Q1grade][Spotn] += 1
    Q2Spot[Q2grade][Spotn] += 1

    outwriter.writerow([barcode, eaglegrade, Sptgrade])
    # else:
    #     print str(barcode) + " X",
    #     missingcount += 1
    #     ##FMfile.seek(0)
    #     ##FMdata.next()
    #

############
# Print it all out
############
print str(missingcount) + ' barcode missing from data'


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
printmatrix(Q1Spot)
printmatrix(Q2Spot)

savematrix(Q1Q2)
savematrix(EQ1)
savematrix(EQ2)

FMfile.close()
hongfile.close()

import csv
import os
import sys
import pyodbc

barcodefile = open(r'F:\Eagle processing\Roke Deep Learning\missing grades.csv')  # list of barcodes
# remove extra first column
barcodedata = csv.DictReader(barcodefile, delimiter=",")
print barcodedata.fieldnames

# ***********************************************************************************************
# ****** For each barcode in the barcode file (stones which have been through Eagle), query*******
# ****** the data base for Q1, Q2, Q3 Spot and Eagle and construct confusion matrices ************
# ************************************************************************************************


# Gradelookup = {'IF': 0, 'VVS1': 1, 'VVS2': 2, 'VS1': 3, 'VS2': 4, 'SI1': 5, 'SI2': 6,
#                'I1': 7,'I2':8, 'I3':9, 'Referral': 10, 'Error':11}
#
# # print Gradelookup.keys()
#
# Q1Q3 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Name': 'Q1 vs Q2/3'}
# EQ1 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#       'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Name': 'Eagle vs Q1'}
# EQ3 = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#       'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Name': 'Eagle vs Q2/3'}
# ESpot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Name': 'Eagle vs Spot'}
# Q1Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Name': 'Q1 vs Spot'}
# Q2Spot = {'IF': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VVS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'VS1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'VS2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SI1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'SI2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'I2':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'I3':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#          'Referral': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Error':[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],'Name': 'Q2/3 vs Spot'}

# Get Barcode
missingcount = 0

conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
cur = conn.cursor()
stonecount = 0

for data_line in barcodedata:
    # print row
    barcode = int(data_line['Barcode'])
    # print barcode

    # Q1grade, Q1sub, Q2grade, Q2sub, Q3grade, Q3sub, Q3Fgrade, Q3Fsub, Sptgrade, Sptsub, eaglegrade = "", "", "", "", \
    #                                                                                                  "", "", "", "", \
    #                                                                                                  "", "", ""
    # eaglegrade = data_line['Grade']
    # if eaglegrade == "":
    #     eaglegrade = "Error"


    #    eaglegrade = data_line[' assigned grade'].strip()
    #    hong_known = data_line['Known grade']
    #    eaglegraden = Gradelookup[eaglegrade]



    querystring = "GetClarityGradingDetails " + str(barcode)
    stonecount += 1
    # print stonecount
    cur.execute(querystring)
    rows = cur.fetchall()

    for row in rows:
        if row and row.MarkingProcess[0:3] != "Col":
            # # print row.MarkingProcess, row.Quality, row.QualitySubGrade
            Grader = row.MarkingProcess
            Quality = row.Quality
            SubGrade = row.QualitySubGrade
            # if Grader == "Quality One":
            #     if Quality != None:
            #         Q1grade = Quality
            #         Q1sub = SubGrade
            # elif Grader == "Quality Two":
            #     if Quality != None:
            #         Q2grade = Quality
            #         Q2sub = SubGrade
            # elif Grader == "Quality Three":
            #     if Quality != None:
            #         Q3grade = Quality
            #         Q3sub = SubGrade
            # elif Grader == "Quality Three Final":
            #     if Quality != None:
            #         Q3Fgrade = Quality
            #         Q3Fsub = SubGrade
            if Grader == "Spot Check":
                if Quality != None:
                    Sptgrade = Quality
                    Sptsub = SubGrade
                    # elif Grader == "Clarity Machine":
                    #     if Quality != None and Quality != "NA":
                    #         eaglegrade = Quality
                    #         #if eaglegrade == "SI1":
                    #           #  sys.exit("Found an SI1!")
                    #         eaglegraden = Gradelookup[eaglegrade]

    print barcode, Sptgrade, Sptsub

# if Q1grade != '' and (Q2grade != '' or Q3grade != '') and Sptgrade != '' and eaglegrade!= '':
#         Q1n = Gradelookup[Q1grade]
#     #    Q2n = Gradelookup[Q2grade]
#         if Q3grade!= '':
#             Q3n = Gradelookup[Q3grade]
#         elif Q2grade != '':
#             Q3n = Gradelookup[Q2grade]
#         Spotn = Gradelookup[Sptgrade]
#
#         Q1Q3[Q1grade][Q3n] += 1
#         EQ1[eaglegrade][Q1n] += 1
#         EQ3[eaglegrade][Q3n] += 1
#         ESpot[eaglegrade][Spotn] += 1
#         Q1Spot[Q1grade][Spotn] += 1
#         if Q3grade != '':
#             Q2Spot[Q3grade][Spotn] += 1
#         else: #if Q2grade == '':
#             Q2Spot[Q2grade][Spotn] += 1
#
# ############
# Print it all out
############
barcodefile.close()
cur.close()
del cur

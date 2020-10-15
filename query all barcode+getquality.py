import os
import pyodbc

folderpath = raw_input("Input the folder path: ")
if folderpath == "":
    folderpath = "S:\Clarity DB 18-09-12 to 05-11-12"


# year=raw_input("input year as yyyy: ")
# if year=="":
#     year = "2013"
# month=raw_input("input month as mm: ")
# if month=="":
#     month="01"

# list barcodes
def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)

    for folder in datefolders:
        stonefolders = os.listdir(os.path.join(folderpath, folder))
        for folders in stonefolders:
            if folders[0] != "c":
                barcodes.append(folders)

                # folderyear=folder[0:4]
                # foldermonth=folder[5:7]
                # if folderyear==year and foldermonth==month:

    return barcodes


barcodes = barcodelist(folderpath)


# for barcode in barcodes:
#    print barcode +"\n",

# go through list of barcodes and query qualities from database

def query_quality(barcodes):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}',
                          SERVER='DTC-CWT-CST-02\FOREVERMARK')  # ,DATABASE='FOREVERMARK')
    cur = conn.cursor()
    qualities = []
    for barcode in barcodes:
        querystring = "GetClarityGradingDetails " + str(barcode)
        # querystring = "SELECT [Quality] FROM [DiamondResearch].[dbo].[ClarityGradingDetails] Where [Barcode]='"+str(barcode)+"' and [GradingTask]='Spot Check'"
        cur.execute(querystring)
        rows = cur.fetchall()
    print "#",

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
    return qualities

Grades = query_quality(barcodes)
# for Q in Grades:
#        print Q

# put Barcode and grade in Dictionary

Qdict = {}
for barcode, grade in zip(barcodes, Grades):
    Qdict[barcode] = grade

for B, G in Qdict.iteritems():
    print B, G


# Save barcode list
def savefile(year, month, barcodes, Qdict):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("Save Barcode list? Y/N ")
        b = a.lower()

    if b == 'y':
        barcodefilename = year + "-" + month + "_withgrades.txt"
        print "Saving File " + barcodefilename + "...."

        outfile = open(barcodefilename, "w")
        outfile.write("Stone Barcodes and qualities for " + month + "/" + year + "\n")
        Q = 0
        for barcode in barcodes:
            outfile.write(barcode + "\t" + Qdict[barcode] + "\n")
        outfile.close()
        print "Done!"
    return


savefile(year, month, barcodes, Qdict)

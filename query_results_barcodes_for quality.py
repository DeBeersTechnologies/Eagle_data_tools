import os
import pyodbc

folderpath = raw_input("Input the folder path: ")
if folderpath == "":
    folderpath = "S:\Clarity DB 18-09-12 to 05-11-12"

year = raw_input("input year as yyyy: ")
if year == "":
    year = "2013"
month = raw_input("input month as mm: ")
if month == "":
    month = "01"


# list barcodes
def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        folderyear = folder[0:4]
        foldermonth = folder[5:7]
        if folderyear == year and foldermonth == month:
            stonefolders = os.listdir(os.path.join(folderpath, folder))
            for folders in stonefolders:
                if folders[0] != "c":
                    barcodes.append(folders)
    return barcodes


barcodes = barcodelist(folderpath)


# for barcode in barcodes:
#    print barcode +"\n",

# go through list of barcodes and query qualities from database

def query_quality(barcodes):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='dtc-fmi-sql-07',
                          DATABASE='DiamondResearch')
    cur = conn.cursor()
    qualities = []
    for barcode in barcodes:
        querystring = "SELECT [Quality] FROM [DiamondResearch].[dbo].[ClarityGradingDetails] Where [Barcode]='" + str(
            barcode) + "' and [GradingTask]='Spot Check'"
        cur.execute(querystring)
        row = cur.fetchone()
        if row:
            Q = row.Quality
            qualities.append(Q)
        else:
            qualities.append("No Spot")
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

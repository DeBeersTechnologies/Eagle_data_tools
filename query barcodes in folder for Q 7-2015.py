import os
import pyodbc


# list barcodes
def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)

    for folder in datefolders:
        stonefolders = os.listdir(os.path.join(folderpath, folder))
        for folders in stonefolders:
            if folders[0] != "c":
                barcodes.append(folders)
    return barcodes


def query_quality(barcodes):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}',
                          SERVER='DTC-CWT-CST-02\FOREVERMARK')  # ,DATABASE='FOREVERMARK')
    cur = conn.cursor()
    qualities = {}
    for barcode in barcodes:
        querystring = "GetClarityGradingDetails " + str(barcode)
        cur.execute(querystring)
        rows = cur.fetchall()
        for row in rows:
            if row and row.MarkingProcess[0:3] != "Col":
                # print row.MarkingProcess, row.Quality, row.QualitySubGrade
                Grader = row.MarkingProcess
                Quality = row.Quality
                SubGrade = row.QualitySubGrade
                if Grader == "Spot Check":
                    Sptgrade = Quality
                    Sptsub = SubGrade
                    if Sptgrade and Sptsub != None:
                        qualities[barcode] = Sptgrade + ' ' + str(Sptsub)

    return qualities


##########
# Main
###########

if __name__ == "__main__":

    folderpath = raw_input("Input the folder path: ")
    if folderpath == "":
        folderpath = r"T:\2015-06-30 onwards clean\Eagle 10"

    Barcodes = barcodelist(folderpath)

    Qual_list = query_quality(Barcodes)

    # print Qual_list

    for barcode in Barcodes:
        if barcode in Qual_list:
            print barcode + ', ' + Qual_list[barcode]

    print str(len(Qual_list)) + " stones in this folder"

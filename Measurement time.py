#################
# Scan folder, get time code for first image and stone wrl
# subtract times, look up quality
#######################
import os
import pyodbc
import shutil
import time
import datetime


def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        if folder[0:3] == "201":
            stonefolders = os.listdir(os.path.join(folderpath, folder))
            for subfolder in stonefolders:
                if subfolder[0] != "c":
                    fullpath = os.path.join(folderpath, folder, subfolder)
                    code_path = (subfolder, fullpath)
                    barcodes.append(code_path)
    return barcodes


def meas_time(barcodes, folder_path):
    times = {}
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        if folder[0:3] == "201":
            stonefolders = os.listdir(os.path.join(folderpath, folder))
            for subfolder in stonefolders:
                if subfolder[0] != "c":
                    fullpath = os.path.join(folderpath, folder, subfolder)
                    xmlpath = os.path.join(fullpath, r"Eaglemeasuredata.xml")
                    first_image_path = os.path.join(fullpath, r"diffuse0\diffuse0-000.png")

                    if os.path.exists(xmlpath):
                        # meas_start = datetime.datetime.fromtimestamp(os.path.getmtime(first_image_path))
                        meas_start = os.path.getctime(first_image_path)
                        # meas_fin = datetime.datetime.fromtimestamp(os.path.getmtime(xmlpath))
                        meas_fin = os.path.getmtime(xmlpath)
                        meastime = (meas_fin - meas_start)
                        # print subfolder, meas_start, meas_fin, meastime
                        times[subfolder] = meastime
                        print "# ",

    return times


def query_quality(barcodes):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}',
                          SERVER='DTC-CWT-CST-02\FOREVERMARK')  # ,DATABASE='FOREVERMARK')
    cur = conn.cursor()
    qualities = {}
    for barcode in barcodes:
        querystring = "GetClarityGradingDetails " + r"'" + str(barcode[0]) + r"'"
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
                        qualities[barcode[0]] = Sptgrade + ' ' + str(Sptsub)
                        print "#",

    return qualities


def savefile(barcodes, qualities, times, folderpath):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("Save Barcode list? Y/N ")
        b = a.lower()

    if b == 'y':
        barcode_file_name = raw_input("Enter Filename: ")
        save_folder = r"c:/"
        save_path = os.path.join(save_folder, barcode_file_name)

        print "Saving File " + barcode_file_name + "...."

        outfile = open(save_path, "w")

        outfile.write("Stones, their qualities and measurement times " + folderpath + "\n")
        for barcode in barcodes:
            if barcode[0] in qualities and barcode[0] in times:
                outfile.write(barcode[0] + ', ' + qualities[barcode[0]] + ', ' + str(times[barcode[0]]) + "\n")
        outfile.close()
        print "Done!"
    return


if __name__ == "__main__":

    # save_path = r"C:\"

    folderpath = raw_input("Input the folder path: ")

    if folderpath == "":
        folderpath = r"T:\2015-06-30 onwards clean\Eagle 10"
        print folderpath

    barcodes = barcodelist(folderpath)
    # print barcodes

    Qual_list = query_quality(barcodes)
    # print Qual_list

    Times = meas_time(barcodes, folderpath)
    # print Times
    savefile(barcodes, Qual_list, Times, folderpath)

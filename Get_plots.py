import urllib
import os
import pyodbc


def barcodelist(folder_path):
    barcodes = []
    stone_folders = os.listdir(folder_path)
    for folder in stone_folders:
        full_path = os.path.join(folder_path, folder)
        if folder[-2] != "_":
            code_path = (folder, full_path)
            barcodes.append(code_path)
    return barcodes


def datefolders(folder_path):
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        full_path = os.path.join(folder_path, folder)


def make_urls(code):
    front_url = r"http://fmgprd.dtc.local/Forevermark/Insecure/StonePlotImage.aspx?barcode=" + \
                code + r"&qualitytask=5&perspective=topdown"
    back_url = r"http://fmgprd.dtc.local/Forevermark/Insecure/StonePlotImage.aspx?barcode=" + \
               code + "&qualitytask=5&perspective=bottomup"

    urls = [front_url, back_url]
    return urls


def ensure_dir(f):
    if not os.path.exists(f):
        os.mkdir(f)


def get_quality(barcode):
    Quality = ""
    SubGrade = ""
    Grade = []
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()
    querystring = "GetClarityGradingDetails " + barcode
    # print querystring
    print "#",
    cur.execute(querystring)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            if row and row.MarkingProcess[0:3] != "Col" and row.MarkingProcess == "Spot Check":
                # print row.MarkingProcess, row.Quality, row.QualitySubGrade

                Quality = row.Quality
                SubGrade = row.QualitySubGrade

            Grade = [Quality, SubGrade]

    return Grade


if __name__ == "__main__":

    folderpath = raw_input("Input the folder path: ")  # folder containing barcode folders

    if folderpath == "":
        folderpath = "H:\Eagle 16"
        print folderpath

    datefolders = datelist(folderpath)
    barcodes = barcodelist(folderpath)

    for barcode in barcodes:
        serial = barcode[0]
        print serial
        urls = make_urls(serial)

        save_path_front = os.path.join(barcode[1], r"grader plots/front_plot.png")
        save_path_back = os.path.join(barcode[1], r"grader plots/back_plot.jpg")
        save_path = os.path.join(barcode[1], r"grader plots")
        save_path_grade = os.path.join(save_path, r"grade.txt")

        ensure_dir(save_path)

        urllib.urlretrieve(urls[0], save_path_front)
        urllib.urlretrieve(urls[1], save_path_back)

        ############ get quality and write ot a text file in the same folder

        grade = get_quality(serial)
        gradefile = open(save_path_grade, 'w')
        gradefile.write(grade[0] + ' ' + str(grade[1]))
        gradefile.close()

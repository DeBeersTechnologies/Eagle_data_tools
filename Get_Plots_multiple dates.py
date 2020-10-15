import urllib
import os
import pyodbc


def barcodelist(folder_path):
    barcodes = []
    stone_folders = os.listdir(folder_path)
    for folder in stone_folders:
        full_path = os.path.join(folder_path, folder)
        if folder[-2] != "_" and folder[0] == "2":
            code_path = (folder, full_path)
            barcodes.append(code_path)
    return barcodes


def datelist(folder_path):
    folderlist = []
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        full_path = os.path.join(folder_path, folder)
        if os.path.isdir(full_path):
            folderlist.append(full_path)
    return folderlist


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

    folderpath = raw_input("Input the folder path: ")  # folder above date folders

    if folderpath == "":
        folderpath = "k:\Eagle 18"
        print folderpath

    stonecount = 0

    datefolders = datelist(folderpath)

    for date in datefolders:

        barcodes = barcodelist(date)

        for barcode in barcodes:
            serial = barcode[0]
            print serial
            stonecount += 1
            urls = make_urls(serial)

            save_path_front = os.path.join(barcode[1], r"grader plots/front_plot.png")
            save_path_back = os.path.join(barcode[1], r"grader plots/back_plot.jpg")
            save_path = os.path.join(barcode[1], r"grader plots")
            save_path_grade = os.path.join(save_path, r"grade.txt")

            ensure_dir(save_path)

            urllib.urlretrieve(urls[0], save_path_front)
            urllib.urlretrieve(urls[1], save_path_back)

            ############ get quality and write ot a text file in the same folder

            if serial[0:3] == '200':
                grade = get_quality(serial)
            else:
                grade = None

            print grade
            if grade and grade[0] and grade[1] != None:
                gradefile = open(save_path_grade, 'w')
                gradefile.write(grade[0] + ' ' + str(grade[1]))
                gradefile.close()

    ### Put stone count in a text file

    print("No. of stones = " + str(stonecount))
    count_file = os.path.join(folderpath, "Stone_count.txt")
    count_file_out = open(count_file, 'w')
    count_file_out.write("No. of stones = " + str(stonecount))
    count_file_out.close()

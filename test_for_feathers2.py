import os
import pyodbc
import shutil


def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        if folder[0:2] == "20":
            stonefolders = os.listdir(os.path.join(folderpath, folder))
            for subfolder in stonefolders:
                if subfolder[0] != "c":
                    fullpath = os.path.join(folderpath, folder, subfolder)
                    code_path = (subfolder, fullpath)
                    barcodes.append(code_path)
    return barcodes


def query_for_feathers(barcodes):
    feather_stone_list = []
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()

    for barcode in barcodes:
        querystring = "GetClarityStonePlotDetails " + '\'' + str(barcode[0]) + '\''
        cur.execute(querystring)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                grader = row.GradingTask
                feature_type = row.PlotFeatures

                if grader == "Spot Check" and feature_type[0:7] == "Feather":
                    # print str(barcode) + " has feather(s)"
                    print '#',
                    feather_stone_list.append(barcode)
                    break
    cur.close()
    return feather_stone_list


def query_quality(feather_stone_list):
    Qualities = {}

    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()

    for stone in feather_stone_list:
        querystring = "GetClarityGradingDetails " + '\'' + str(stone[0]) + '\''
        cur.execute(querystring)
        rows = cur.fetchall()
        if rows:
            for row in rows:
                grader = row.MarkingProcess
                quality = row.Quality
                if grader == "Spot Check":
                    Qualities[stone[0]] = quality
                    print '#',
                    break

    cur.close()
    return Qualities


def savefile(stonelist, qualities, folderpath):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("Save Barcode list? Y/N ")
        b = a.lower()

    if b == 'y':
        barcode_file_name = raw_input("Enter Filename: ")
        save_folder = r"F:\Eagle processing\feathers"
        save_path = os.path.join(save_folder, barcode_file_name)

        print "Saving File " + barcode_file_name + "...."

        outfile = open(save_path, "w")

        outfile.write("Stones containing  feathers in  folder with their qualities " + folderpath + "\n")
        for stone in stonelist:
            outfile.write(stone[0] + ', ' + qualities[stone[0]] + "\n")
        outfile.close()
        print "Done!"
    return


def copy_folders(storage_path, List_of_stones):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("copy folders to " + storage_path + " Y/N ?")
        b = a.lower()

    if b == 'y':

        for item in List_of_stones:
            n = 0
            inpath = item[1]
            outpath = os.path.join(storage_path, item[0])
            if os.path.exists(outpath):
                outpath = os.path.join(storage_path, item[0] + '_' + str(n))
                n = + 1
            shutil.copytree(inpath, outpath)
            print '#',


if __name__ == "__main__":

    folderpath = raw_input("Input the folder path: ")
    if folderpath == "":
        folderpath = "T:\Eagle 10"
        print folderpath

    storage_path = r"g:\Feathers\Eagle 14"

    # print barcodelist(folderpath)

    barcodes = barcodelist(folderpath)
    List_of_stones = query_for_feathers(barcodes)

    print '\n'
    # print List_of_stones

    qual_dict = query_quality(List_of_stones)

    print qual_dict

    savefile(List_of_stones, qual_dict, folderpath)

    copy_folders(storage_path, List_of_stones)

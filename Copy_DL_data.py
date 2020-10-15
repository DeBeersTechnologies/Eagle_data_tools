import os
import pyodbc
import shutil
import Get_plots


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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


def ensure_dir(f):
    if not os.path.exists(f):
        os.mkdir(f)


if __name__ == "__main__":

    folderpath = raw_input("Input the folder path: ")  # folder above date folders
    # Machine_No = raw_input("Input Machine no. ")
    Machines = [10, 11, 12, 14, 15, 16, 17]

    for Machine_No in Machines:

        copycount = 0

        disk_path = os.path.join("G:\Deep_Learning_data", "Eagle " + str(Machine_No))

        if folderpath == "":
            folderpath = r"Q:\2016"
            print folderpath

        datefolders = datelist(os.path.join(folderpath, "Eagle " + str(Machine_No)))

        for date in datefolders:

            barcodes = barcodelist(date)

            if (len(barcodes) == 1 and barcodes[0] == 'calibration') or len(barcodes) == 0 or barcodes == None:
                print "no stones"

            else:
                for barcode in barcodes:

                    folder_scan = os.listdir(barcode[1])

                    if len(folder_scan) <= 2:
                        print barcode[1] + " is an empty folder!"
                        break  # go to next barcode if empty
                    else:
                        date_foldername = os.path.split(date)
                        print 'Machine: ' + str(Machine_No), date_foldername[1], barcode[0]
                        shutil.copytree(barcode[1], os.path.join(disk_path, date_foldername[1], barcode[0]))
                        copycount += 1

        print str(copycount) + " Stones copied"

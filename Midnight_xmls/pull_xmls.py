import os
import pyodbc
import shutil


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
    return datefolders


def ensure_dir(f):
    if not os.path.exists(f):
        os.mkdir(f)


def get_xmls(barcode):
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()
    Sarinquerystring = "SELECT sr.OriginalXml [SarinXml] FROM SarinRecord sr \
            JOIN Task t ON sr.TaskId = t.TaskId \
            JOIN Parcel p ON t.ParcelId = p.ParcelId WHERE p.CustomerBarcode = " + barcode + " AND sr.IsLatest = 1"
    cur.execute(Sarinquerystring)
    Sarinxml = cur.fetchone()

    Falconquerystring = "Select top 1 cmr.OriginalXml [FalconXml] from ColourMachineRecord cmr\
    JOIN ColourRecord cr on cmr.ColourRecordId = cr.ColourRecordId JOIN task t on cr.TaskId = t.TaskId\
    JOIN Parcel p ON t.ParcelId = p.ParcelId WHERE  p.CustomerBarcode = " + barcode
    cur.execute(Falconquerystring)
    Falconxml = cur.fetchone()
    # print"SARIN"
    # print (Sarinxml[0])
    # print"falcon"
    # print (Falconxml[0])

    cur.close
    return Sarinxml[0], Falconxml[0]


if __name__ == "__main__":

    # xmls = get_xmls('20002276617')
    # print(xmls[0])
    # print ""
    # print(xmls[1])


    folderpath = raw_input("Input the folder path: ")  # folder containing barcode folders

    if folderpath == "":
        folderpath = "G:\Eagle 11"
        print folderpath
    outputfolder = "F:\Midnight"

    # get list of dates
    dates = datefolders(folderpath)
    count = 0
    for datefolder in dates:
        thisdatefolder = os.path.join(folderpath, datefolder)
        barcodes = barcodelist(thisdatefolder)
        for barcode in barcodes:
            if barcode[0] != 'calibration' and os.path.isdir(barcode[1]):
                thisbarcodefolder = os.path.join(thisdatefolder, str(barcode[0]))
                savepath = os.path.join(outputfolder, str(barcode[0]))
                ensure_dir(savepath)
                savesarin = os.path.join(savepath, r"Sarin.xml")
                savefalcon = os.path.join(savepath, r"Falcon.xml")
                serial = barcode[0]
                eaglewrlpath = os.path.join(thisbarcodefolder, (str(barcode[0]) + ".wrl"))
                if os.path.exists(eaglewrlpath):
                    shutil.copy(eaglewrlpath, savepath)
                    print serial
                    xmls = get_xmls(serial)
                    sarinefile = open(savesarin, 'w')
                    sarinefile.write(xmls[0])
                    sarinefile.close()
                    Falconfile = open(savefalcon, 'w')
                    Falconfile.write(xmls[1])
                    Falconfile.close()
                    count += 1

    Print("Finished! " + str(count) + " stone's data copied.")

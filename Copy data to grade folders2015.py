import os
import pyodbc
import shutil

# year=raw_input("input year as yyyy: ")
# if year == "":
#     year = "2013"
# month=raw_input("input month as mm: ")
# if month == "":
#     month="01"

## Hong Path must exist
Hongpath = r"X:\Hong\2015 Batch 3"  # r"F:\Eagle processing\testcopy"

############
## Folder path is folder where barcode folders are
#############

folderpath = raw_input("Input the folder path to scan. Leave Blank for default: ")
if folderpath == "":
    folderpath = r"F:\Eagle processing\402GRPbuild\Results"
barcodes = os.listdir(folderpath)
Qualdict = {}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


############
# Query all Qualities for one barcode.
############

def query_quality(barcode):
    Q1grade = ""
    Q2grade = ""
    Q3grade = ""
    Q3Fgrade = ""
    Q1sub = ""
    Q2sub = ""
    Q3sub = ""
    Q3Fsub = ""
    Sptgrade = ""
    Sptsub = ""
    Gradelist = []
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-FMI-SQL-13\FOREVERMARK')
    cur = conn.cursor()
    querystring = "GetClarityGradingDetails " + barcode
    # print querystring
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

        Gradelist = [Q1grade, Q1sub, Q2grade, Q2sub, Q3grade, Q3sub, Q3Fgrade, Q3Fsub, Sptgrade, Sptsub]

    return Gradelist


#################
# Save data to csv
#################

def savefile(year, month, barcodes, Qualdict):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("Save Barcode list? Y/N ")
        b = a.lower()

    if b == 'y':
        stopdupes = 1

        barcodefilename = year + "-" + month + "_" + str(stopdupes) + "_allgrades.txt"
        while os.path.exists(barcodefilename):
            stopdupes += 1
            barcodefilename = year + "-" + month + "_" + str(stopdupes) + "_allgrades.txt"

        ##        if os.path.exists(barcodefilename):
        ##            barcodefilename=year+"-"+month+"_allgrades.txt"

        print "Saving File " + barcodefilename + "...."

        outfile = open(barcodefilename, "w")
        outfile.write("Stone Barcodes and qualities for " + month + "/" + year + "\n")
        outfile.write("Barcode , Q1 , Q1sub , Q2 , Q2sub , Q3 , Q3sub , Q3F , Q3Fsub , Spot , Spotsub \n")

        Q = 0
        for barcode in barcodes:
            if barcode in Qualdict:
                outfile.write(barcode + ",")
                for i in range(0, 10):
                    quals = Qualdict[str(barcode)][i]
                    outfile.write(str(quals) + ",")
                outfile.write("\n")
                print "#",

        outfile.close()
        print "Done!"
    return


## copied track and clusterfiles to Hong's folders

def copy_data_files(folderpath, Qdict, Hongpath):
    # copies spot results to Hongpath

    ## ask whether to do it!
    a, b = '', ''
    while b != 'y' and b != 'n':
        a = raw_input("Copy files for Hong? Y/N ")
        b = a.lower()

    if b == 'y':
        # Hongpath='X:\\Hong\\'
        # trackfile='stone.tk'
        # clustfile='stone.clust'
        print "Copying Files..... please wait."
        stonefolders = os.listdir(folderpath)
        for stnfolder in stonefolders:
            # if stnfolder[0]!= "c":
            if stnfolder.isdigit() == True and stnfolder in Qdict:
                Qual = str(Qdict[stnfolder][8]) + "\\"
                Subqual = str(Qdict[stnfolder][9])
                print stnfolder, Qual, Subqual + " ",
                print Qdict[stnfolder]
                QHongpath = os.path.join(Hongpath, Qual, Subqual)
                if os.path.exists(os.path.join(Hongpath, Qual)) == False:
                    os.mkdir(os.path.join(Hongpath, Qual))
                if os.path.exists(QHongpath) == False:
                    os.mkdir(QHongpath)
                curstnfolder = os.path.join(folderpath, stnfolder)
                # curtrkfile=os.path.join(curstnfolder,trackfile)
                # curclstfile=os.path.join(curstnfolder,clustfile)
                # if os.path.exists(curtrkfile)and os.path.exists(curclstfile):
                if os.path.exists(os.path.join(QHongpath, stnfolder)) == False and os.listdir(curstnfolder) != "":
                    diafile = stnfolder + ".dia"
                    if os.path.exists(os.path.join(curstnfolder, diafile)):
                        os.remove(os.path.join(curstnfolder, diafile))
                    shutil.copytree(curstnfolder, os.path.join(QHongpath, stnfolder))

        print "\n Done!"


##########
# Main
###########

if __name__ == "__main__":

    for barcode in barcodes:
        Qlist = query_quality(barcode)
        if Qlist != []:  # make sure there are there are some qualities
            Qualdict[str(barcode)] = Qlist

    print str(len(Qualdict)) + " Stones in Folder"

    # savefile(year, month, barcodes, Qualdict)
    copy_data_files(folderpath, Qualdict, Hongpath)

# could pass Q1, Q2 etc to copy_tk_clust to re-do for other graders

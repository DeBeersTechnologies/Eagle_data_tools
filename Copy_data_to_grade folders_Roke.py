import os
import pyodbc
import shutil
import Get_plots
import urllib


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# list barcodes

def barcodelist(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)
    for folder in datefolders:
        if os.path.isdir(os.path.join(folderpath, folder)):
            stonefolders = os.listdir(os.path.join(folderpath, folder))
            for folders in stonefolders:
                if folders.isdigit():
                    barcodes.append(folders)
                    # if folders[0]!= "c":

    # folderyear = folder[0:4]
    #     foldermonth = folder[5:7]
    # if folderyear == year and foldermonth == month:

    return barcodes


#
# Query all Qualities for one barcode.
#


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
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
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
    cur.close()
    return Gradelist


# Save data to csv

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

def Copy_data_files(folderpath, Out_file_path, Qdict):
    # copies spot results to Out_file_path

    ## ask whether to do it!
    a, b = '', ''
    while b != 'y' and b != 'n':
        a = raw_input("Copy files for Hong? Y/N ")
        b = a.lower()

    if b == 'y':
        # Out_file_path='X:\\Hong\\'
        # trackfile='stone.tk'
        # clustfile='stone.clust'
        datefolders = os.listdir(folderpath)
        print "Copying Files..... please wait."
        for datefolder in datefolders:
            # folderyear=datefolder[0:4]
            # foldermonth=datefolder[5:7]
            # if folderyear==year and foldermonth==month:
            if os.path.isdir(os.path.join(folderpath, datefolder):
                stonefolders = os.listdir(os.path.join(folderpath, datefolder))
            for stnfolder in stonefolders:
            # if stnfolder[0]!= "c":
                if
            stnfolder.isdigit() and stnfolder in Qdict:
            Qual = str(Qdict[stnfolder][8]) + "\\"
            Subqual = str(Qdict[stnfolder][9])
            print stnfolder, Qual, Subqual + " ",
            print Qdict[stnfolder]
            Qual_Out_file_path = os.path.join(Out_file_path, Qual, Subqual)
            if os.path.exists(os.path.join(Out_file_path, Qual)) == False:
                os.mkdir(os.path.join(Out_file_path, Qual))
            if os.path.exists(Qual_Out_file_path) == False:
                os.mkdir(Qual_Out_file_path)
            curstnfolder = os.path.join(folderpath, datefolder, stnfolder)
            # curtrkfile=os.path.join(curstnfolder,trackfile)
            # curclstfile=os.path.join(curstnfolder,clustfile)
            # if os.path.exists(curtrkfile)and os.path.exists(curclstfile):
            # if not os.path.exists(Qual_Out_file_path):
            # os.mkdir(Qual_Out_file_path)

            outputfolder = os.path.join(Qual_Out_file_path, stnfolder)
            dupe = 1

            if os.path.exists(outputfolder):
                while os.path.exists(os.path.join(outputfolder, "_" + str(dupe))):
                    dupe += 1
            outputfolder = os.path.join(outputfolder, "_" + str(dupe))

            # if not os.path.exists(outputfolder):

            shutil.copytree(curstnfolder, outputfolder
                            , symlinks=False, ignore=None)
            # get plots and put in samee folder
            print "getting plots..."
            plot_urls = Get_plots.make_urls(stnfolder)
            save_path_front = os.path.join(outputfolder, r"grader plots/front_plot.png")
            save_path_back = os.path.join(outputfolder, r"grader plots/back_plot.jpg")
            save_path = os.path.join(outputfolder, r"grader plots")
            Get_plots.ensure_dir(save_path)
            urllib.urlretrieve(plot_urls[0], save_path_front)
            urllib.urlretrieve(plot_urls[1], save_path_back)

            # shutil.copy2(os.path.join(curstnfolder,clustfile),os.path.join(Qual_Out_file_path,stnfolder),,)

    print "\n Done!"


if __name__ == "__main__":
    folderpath = raw_input("Input the folder path to scan: ")
    if folderpath == "":
        folderpath = "T:\Eagle 10"
    print folderpath
    # year=raw_input("input year as yyyy: ")
    # if year == "":
    #     year = "2013"
    # month=raw_input("input month as mm: ")
    # if month == "":
    #     month="01"

    Out_file_path = r"G:\Graded data"
    # must exist
    barcodes = barcodelist(folderpath)

    Qualdict = {}

    for barcode in barcodes:
        Qlist = query_quality(barcode)
        if Qlist != []:  # make sure there are there are some qualities
            Qualdict[str(barcode)] = Qlist

    print str(len(Qualdict)) + " Stones"  # in "+str(month)+"/"+str(year)

    # savefile(year, month, barcodes, Qualdict)
    Copy_data_files(folderpath, Out_file_path, Qualdict)

# could pass Q1, Q2 etc to Copy_data_files to re-do for other graders

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
    conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
    cur = conn.cursor()
    qualities = {}
    for barcode in barcodes:
        querystring = "GetClarityGradingDetails " + str(barcode)
        customer_query = "select c.Name, CustomerBarcode from Parcel p inner join Import i on i.ImportId =" \
                         " p.ImportId inner join Customer c on c.customerid = i.customerid where CustomerBarcode " \
                         "= " + barcode
        cur.execute(querystring)
        rows = cur.fetchall()
        cur.execute(customer_query)
        cust = cur.fetchall()

        for row in cust:
            customer = row.Name

        for row in rows:
            if row and row.MarkingProcess[0:3] != "Col":
                # print row.MarkingProcess, row.Quality, row.QualitySubGrade
                Grader = row.MarkingProcess
                Quality = row.Quality
                SubGrade = row.QualitySubGrade
                if Grader == "Spot Check" and (Quality and SubGrade != None):
                    Sptgrade = Quality + ", "
                    Sptsub = str(SubGrade) + ", "
                    qualities[barcode] = Sptgrade + Sptsub + customer
                    print "#",

    cur.close()

    return qualities


##########
# Main
###########

if __name__ == "__main__":

    folderpath = raw_input("Input the folder path: ")
    if folderpath == "":
        folderpath = r"T:\2015-06-30 onwards clean\Eagle 18"

    Barcodes = barcodelist(folderpath)

    Qual_list = query_quality(Barcodes)

    # print Qual_list

    for barcode in Barcodes:
        if barcode in Qual_list:
            print barcode + ', ' + Qual_list[barcode]

    print str(len(Qual_list)) + " stones in this folder"

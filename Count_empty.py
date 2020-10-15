import os

folderpath = raw_input("Input the folder path to scan. Leave Blank for default: ")
if folderpath == "":
    folderpath = r"F:\Eagle processing\402GRPbuild\Results"

barcodes = os.listdir(folderpath)

No_of_barcodes = len(barcodes)
Empty_count = 0

for barcode in barcodes:
    data_path = os.path.join(folderpath, barcode)
    if os.listdir(data_path) == []:
        Empty_count += 1

print str(Empty_count) + ' empty folders out of ' + str(No_of_barcodes) + " Folders" \
                                                                          "                                                                           ""

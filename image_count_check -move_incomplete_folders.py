import os, shutil

############################
# Path to check for missing images
############################
folderpath = (r'T:\2015-06-30 onwards clean\eagle 15')


def check_folder(folder_path):
    movefolders = "y"
    barcodes = []
    datefolders = os.listdir(folder_path)
    no_of_images = 0

    # go through date folders and find stone (barcode) folders

    for folder in datefolders:
        stonefolders = os.listdir(os.path.join(folderpath, folder))
        n = 0
        for folders in stonefolders:

            if folders[0] != "c":  # if not a calib
                barcodes.append(folders)  # add to barcode list
                this_folder = os.path.join(folderpath, folder, folders, r"diffuse0")  # diffuse0 folder
                if os.path.exists(this_folder):  # if there is no diff0 folder, there are no images at all
                    no_of_images = len(os.listdir(this_folder))
                    if no_of_images < 200:  # < 200 means incomplete
                        print this_folder + " has only " + str(no_of_images) + " images"
                        # movefolders = raw_input("move incomplete folder?(irreversible) y/n ")
                        if movefolders == "":
                            movefolders = "n"
                        if movefolders == "y":
                            print "moving"
                            inpath = os.path.join(folderpath, folder, folders)
                            eagleno = folderpath[-8:len(folderpath)]  # last 8 characters of folderpath
                            dest_folder = (r"T:\2015-06-30 onwards clean\Empty folders")  # where to move things
                            outpath = os.path.join(dest_folder, eagleno, folders)
                            while os.path.exists(outpath):
                                n = n + 1
                                folders = folders + "(" + str(n) + ")"
                                outpath = os.path.join(dest_folder, eagleno, folders)
                            shutil.copytree(inpath, outpath)
                            shutil.rmtree(inpath)
                            print "done"

                else:  # do this is no images at all
                    print this_folder + " has no images"
                    # uncomment below if you want to check each
                    # movefolders = raw_input("move empty folder?(irreversible) y/n ")

                    if movefolders == "":
                        movefolders = "n"
                    if movefolders == "y":
                        print "moving"
                        inpath = os.path.join(folderpath, folder, folders)
                        eagleno = folderpath[-8:len(folderpath)]
                        dest_folder = (r"T:\2015-06-30 onwards clean\Empty folders")
                        outpath = os.path.join(dest_folder, eagleno, folders)
                        while os.path.exists(outpath):
                            n = n + 1
                            folders = folders + "(" + str(n) + ")"
                            outpath = os.path.join(dest_folder, eagleno, folders)
                        shutil.copytree(inpath, outpath)  # copy
                        shutil.rmtree(inpath)  # delete original
                        print "done"

    return (barcodes)


check_folder(folderpath)

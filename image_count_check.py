import os, shutil

folderpath = (r'G:\2015-06-30 onwards clean\eagle 18')


def check_folder(folder_path):
    barcodes = []
    datefolders = os.listdir(folder_path)
    no_of_images = 0
    for folder in datefolders:
        stonefolders = os.listdir(os.path.join(folderpath, folder))
        for folders in stonefolders:
            if folders[0] != "c":
                barcodes.append(folders)
                this_folder = os.path.join(folderpath, folder, folders, r"diffuse0")
                if os.path.exists(this_folder):
                    no_of_images = len(os.listdir(this_folder))
                    if no_of_images < 200:
                        print this_folder + " has only " + str(no_of_images) + " images"
                        removefolders = raw_input("Remove incomplete folder?(irreversible) y/n ")
                        if removefolders == "":
                            removefolders = "n"
                        if removefolders == "y":
                            print "removing"
                            shutil.rmtree(os.path.join(folderpath, folder, folders))
                            print "done"

                else:
                    print this_folder + " has no images"
                    removefolders = raw_input("Remove empty folder?(irreversible) y/n ")
                    if removefolders == "":
                        removefolders = "n"
                    if removefolders == "y":
                        print "removing"
                        shutil.rmtree(os.path.join(folderpath, folder, folders))
                        print "done"

    return (barcodes)


check_folder(folderpath)


def copy_folders(storage_path, List_of_stones):
    a, b = '', ''

    while b != 'y' and b != 'n':
        a = raw_input("copy folders to " + storage_path + " Y/N ?")
        b = a.lower()

    if b == 'y':
        n = 0

        for item in List_of_stones:

            inpath = item[1]
            outpath = os.path.join(storage_path, item[0])
            if os.path.exists(outpath):
                outpath = os.path.join(storage_path, item[0] + '_' + str(n))
                n = + 1
            shutil.copytree(inpath, outpath)
            print '#',

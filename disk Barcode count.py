import os

diskname = "k:\\"
barcode_count = 0
machine_names = os.listdir(diskname)

for machine in machine_names:
    machine_path = os.path.join(diskname, machine)
    if os.path.isdir(machine_path) and machine[0:6] != "System":
        date_folders = os.listdir(machine_path)
        for date in date_folders:
            barcodes_path = os.path.join(machine_path, date)
            if os.path.isdir(barcodes_path):
                barcode_list = os.listdir(barcodes_path)
                for barcode in barcode_list:
                    if len(barcode) == 11 and barcode[0:2] == "20":
                        barcode_count += 1
                        print barcode_count

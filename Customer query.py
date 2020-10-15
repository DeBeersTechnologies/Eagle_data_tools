import csv
import os
import pyodbc

conn = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', SERVER='DTC-CWT-CST-02\FOREVERMARK')
cur = conn.cursor()

barcode = "20001788214"

sql_command = "select c.Name, CustomerBarcode from Parcel p inner join Import i on i.ImportId = p.ImportId inner join Customer c on c.customerid = i.customerid where CustomerBarcode = " + barcode

cur.execute(sql_command)

rows = cur.fetchall()
for row in rows:
    print row

cur.close()

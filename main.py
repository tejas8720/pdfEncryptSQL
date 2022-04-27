from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import urllib.parse
import sqlalchemy
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
import time

password = urllib.parse.quote_plus("******")  # '123%40456'
tablename = 'encryptedFiles'
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/sql_training')
meta = MetaData()

if sqlalchemy.inspect(engine).has_table(tablename):
    pass
else:
    tb = Table(tablename, meta,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('name', String(60), nullable=False),
                      Column('size', String(60), nullable=False),
                      Column('time', String(60), nullable=False),
                      )
    tb.create(engine)

files = os.listdir(r"./pdf")
i=1
for f in files:
    with open('./pdf/'+f, "rb") as in_file:
        input_pdf = PdfFileReader(in_file)
        output_pdf = PdfFileWriter()
        output_pdf.appendPagesFromReader(input_pdf)
        output_pdf.encrypt(f)
        filename1 = datetime.now().strftime("%Y_%m_%d-%H:%M:%S")
        file_size = os.path.getsize('./pdf/'+f)
        tm = datetime.now().strftime("%H:%M:%S")
        engine.execute("INSERT INTO  `encryptedFiles` VALUES ('{}','{}','{}','{}')".format(i,f+'_'+filename1,str(file_size)+' bytes', tm))
        with open('./pdf/'+f+'_'+filename1, "wb") as out_file:
            output_pdf.write(out_file)
        time.sleep(2)
        i+=1



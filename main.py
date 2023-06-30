import xlsxwriter
from companyProcessing import qualcommComp,cienaComp,adobeComp,paypalComp,intelComp,bakerhughesComp,yahooComp,mcafeeComp
import threading

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('JobPostings.xlsx')
cell_format = workbook.add_format()
cell_format.set_bold()      # Turns bold on.
cell_format.set_bold(True)  # Also turns bold on.
# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

lock = threading.Lock()

# creating threads
t1 = threading.Thread(target=cienaComp, args=(lock,worksheet,cell_format))
t2 = threading.Thread(target=adobeComp, args=(lock,worksheet,cell_format))
t3 = threading.Thread(target=qualcommComp, args=(lock,worksheet,cell_format))
t4 = threading.Thread(target=paypalComp, args=(lock,worksheet,cell_format))
t5 = threading.Thread(target=intelComp, args=(lock,worksheet,cell_format))
t6 = threading.Thread(target=bakerhughesComp, args=(lock,worksheet,cell_format))
t7 = threading.Thread(target=yahooComp, args=(lock,worksheet,cell_format))
t8 = threading.Thread(target=mcafeeComp, args=(lock,worksheet,cell_format))
# start threads
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
# wait until threads finish their job
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()

workbook.close()
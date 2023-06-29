import xlsxwriter
from companyProcessing import qualcommComp,cienaComp,adobeComp
import threading

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('JobPostings.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

lock = threading.Lock()

# creating threads
t1 = threading.Thread(target=cienaComp, args=(lock,worksheet))
t2 = threading.Thread(target=adobeComp, args=(lock,worksheet))
t3 = threading.Thread(target=qualcommComp, args=(lock,worksheet))

# start threads
t1.start()
t2.start()
t3.start()
# wait until threads finish their job
t1.join()
t2.join()
t3.join()

workbook.close()
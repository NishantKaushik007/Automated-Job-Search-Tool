import xlsxwriter
import threading
import companyProcessing
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
companies = ["ciena","adobe","qualcomm","paypal","intel","bakerhughes","yahoo","mcafee"]
threads = []
for i in companies:
    t = threading.Thread(target=getattr(companyProcessing,i+'Comp'), args=(lock,worksheet,cell_format))
    threads.append(t)

for i in threads:
    i.start()

for i in threads:
    i.join()

workbook.close()
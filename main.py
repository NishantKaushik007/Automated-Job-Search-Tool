import xlsxwriter
import threading
import companyProcessing
import os
from companyProcessing import getCompanyData
from sendEmail import sendMail
from telegram_bot import sendToTelegram

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
companies = ["ciena","adobe","qualcomm","paypal","intel","bakerhughes","yahoo","mcafee","airbus","alfa laval","cae","dentsu","finastra","diageo","hp","kone","philips","lseg","samsung","siemens gamesa","snc lavalin","sun life","swift","wolters kluwer","nissan","old mutual","nxp","auto desk","wells fargo","arrow","vm ware","cadence","rakuten","pwc","hitachi","equinity","ntt","becton dickinson","taskus","morningstar","factset","unisys","gartner","bristlecone","software ag","target","nvidia","sprinklr","broadcom","broadridge","fico","saxobank","s&p global","caterpillar","heinz","flowserve","fractal","travelex","taylormadegolf","amadeus","nasdaq","franklintempleton","blueyonder","perkinelmer","veritas","flsmidth","icon","cyient","cerence","iqvia","deutsche bank","citi","walmart","manhattan associates","equifax","boeing","dell","dxc technology","flex","jll","wabtec","applied materials","mastercard","thales","pitney bowes","alcon","motorola solutions","stanley black decker","mavenir","trans union","natwest","cdk global","sensata","bread financial","trimble","semtech","pentair","fnz","millennium","snapchat","king","kyndryl"]
threads = []
for i in companies:
    t = threading.Thread(target=getCompanyData, args=(i,lock,worksheet,cell_format))
    threads.append(t)

for i in threads:
    i.start()

for i in threads:
    i.join()

worksheet.autofit()
workbook.close()

file = open('JobPostings.xlsx')

# get the cursor positioned at end
file.seek(0, os.SEEK_END)

# get the current position of cursor
# this will be equivalent to size of file
print("Size of file is :", file.tell(), "bytes")
sendMail()
sendToTelegram()
file.close()
os.remove('JobPostings.xlsx')
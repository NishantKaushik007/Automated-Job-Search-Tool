import os
from mailjet_rest import Client
import base64
import math
from dotenv import load_dotenv
from readExcel import readExcel

def sendMail():
    load_dotenv()
    # read by default 1st sheet of an excel file
    data = open('JobPostings.xlsx', 'rb').read()
    base64_encoded = base64.b64encode(data).decode('UTF-8')
    # print(base64_encoded)
    api_key = os.getenv('Api_Key')
    api_secret = os.getenv('Api_Secret')
    # template_id = os.getenv('TEMPLATE_ID')
    df = readExcel()
    chunk_size = 49

    x = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

    for i in x:
        dict = []
        for j in i.values:
            pair = {'Name': j[0], 'Email': j[1]}
            dict.append(pair)

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "nishant.nishantkaushik.nishant@gmail.com",
                        "Name": "AUTOMATED-JOB-SEARCH-TOOL"
                    },
                    "To": [
                    {
                        "Email": "nishant.nishantkaushik.nishant@gmail.com",
                        "Name": "AUTOMATED-JOB-SEARCH-TOOL"
                    }
                    ],
                    "Bcc": dict,
                    "TemplateID": 4925584,
                    "TemplateLanguage": True,
                    "Subject": "Daily Job Openings !!",
                    "Attachments": [
                        {
                            "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            "Filename": "JobPostings.xlsx",
                            "Base64Content": base64_encoded
                        }
                    ]
                }
            ]
        }

        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
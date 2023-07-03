import requests
from datetime import date
import os
from dotenv import load_dotenv

def sendToTelegram():
    load_dotenv()
    bot_token = '6391669202:AAF9B0vCiJT8rBKj-TET05Lv4dsUC6SNGtM'
    channel_id = '@automatedJobSearchTool'
    file_path = 'JobPostings.xlsx'
    today = date.today()

    # Read the contents of the HTML file
    with open('TelegramMsgBody.txt', 'r') as file:
        html_content = file.read()

    url = f'https://api.telegram.org/bot{bot_token}/sendDocument?chat_id={channel_id}'

    message_data = {'caption': html_content}
    files = {'document': (str('JobPostings '+str(today)+'.xlsx'),open(file_path, 'rb'))}

    response = requests.post(url, data=message_data, files=files)
    try:
        if response.status_code == 200:
            print('File sent successfully.')
        else:
            print(f'Error sending file: {response.json()}')
    except requests.exceptions.HTTPError as errh:
        print('Error : ',errh.args[0])
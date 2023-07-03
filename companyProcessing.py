import requests
import bs4
import json
import threading

data = json.load(open('companiesData.json', 'r'))

row = 0
def initComp(tokenURL,jobURL,payload):
    text = requests.get(tokenURL).text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    data = soup.find_all("script")[0].text.strip()

    index = data.find("token")
    start = index + 8
    end = start + 36
    token = data[start:end]
    headers = {'content-type': 'application/json'}
    url = str(jobURL)
    params = {'X-CALYPSO-CSRF-TOKEN': token}

    print(threading.currentThread().getName().partition("(getCompanyData)")[0], token, '    ', tokenURL)

    response = requests.post(url, params=params, data=json.dumps(payload), headers=headers)

    data = response.json()

    jobsDictionary = []
    for i in data['jobPostings']:
        Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
               'postedOn': i['postedOn']}
        jobsDictionary.append(Job)
    return jobsDictionary

def writeToExcel(title,jobsDictionary,worksheet,cell_format):
    global row
    row += 2
    worksheet.write(row, 0, str(title).upper(),cell_format)
    row += 1
    worksheet.write(row, 0, 'Job Title',cell_format)
    worksheet.write(row, 1, 'Job Id',cell_format)
    worksheet.write(row, 2, 'Location',cell_format)
    worksheet.write(row, 3, 'Posted On',cell_format)
    row += 1
    # iterating through content list
    for item in jobsDictionary:
        column = 0
        for i in ['jobTitle', 'jobId', 'location', 'postedOn']:
            # write operation perform
            worksheet.write(row, column, item[i])
            column += 1
        # incrementing the value of row by one
        # with each iterations.
        row += 1


def getCompanyData(companyName,lock,worksheet,cell_format):
    jobsDictionary = initComp(data['companies'][0][str(companyName)]['tokenURL'],data['companies'][0][str(companyName)]['jobURL'],data['companies'][0][str(companyName)]['payload'])
    lock.acquire()
    writeToExcel(companyName+' Company', jobsDictionary, worksheet,cell_format)
    lock.release()
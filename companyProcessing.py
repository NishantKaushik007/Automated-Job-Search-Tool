import requests
import bs4
import json

row = 0
def initComp(tokenURL,start,end,jobURL,payload):
    text = requests.get(tokenURL).text
    soup = bs4.BeautifulSoup(text, features='html.parser')
    data = soup.find_all("script")[0].text.strip()[start:end]
    data = data.replace(":", "\":")
    data = data.replace("  ", "\"")

    print(data)
    headers = {'content-type': 'application/json'}
    url = jobURL
    params = {'X-CALYPSO-CSRF-TOKEN': data}

    response = requests.post(url, params=params, data=json.dumps(payload), headers=headers)

    data = response.json()

    jobsDictionary = []
    for i in data['jobPostings']:
        Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
               'postedOn': i['postedOn']}
        jobsDictionary.append(Job)
    return jobsDictionary

def writeToExcel(title,jobsDictionary,worksheet):
    global row
    row += 2
    worksheet.write(row, 0, title)
    row += 1
    worksheet.write(row, 0, 'jobTitle')
    worksheet.write(row, 1, 'jobId')
    worksheet.write(row, 2, 'location')
    worksheet.write(row, 3, 'postedOn')
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

def qualcommComp(lock,worksheet):
    payload = {
        "appliedFacets": {},
        "limit": 10,
        "offset": 0
    }
    jobsDictionary = initComp(tokenURL='https://qualcomm.wd5.myworkdayjobs.com/External',start=494,end=530,jobURL='https://qualcomm.wd5.myworkdayjobs.com/wday/cxs/qualcomm/External/jobs',payload=payload)
    lock.acquire()
    writeToExcel('Qualcomm Company', jobsDictionary, worksheet)
    lock.release()

def cienaComp(lock,worksheet):
    payload = {
        "appliedFacets": {},
        "limit": 10,
        "offset": 0
    }
    jobsDictionary = initComp('https://ciena.wd5.myworkdayjobs.com/en-US/Careers',672,708,'https://ciena.wd5.myworkdayjobs.com/wday/cxs/ciena/Careers/jobs',payload)
    lock.acquire()
    writeToExcel('Ciena Company',jobsDictionary,worksheet)
    lock.release()


def adobeComp(lock,worksheet):
    payload = {"appliedFacets":{"jobFamilyGroup":["591af8b812fa10737af39db3d96eed9f"],"locationCountry":["c4f78be1a8f14da0ab49ce1162348a5e"],"locations":["3ba4ecdf4893100bc84aa7a3f1e46b98","3ba4ecdf4893100bc84a8e6d38d46b70"]},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp('https://adobe.wd5.myworkdayjobs.com/external_experienced?jobFamilyGroup=591af8b812fa10737af39db3d96eed9f&locationCountry=c4f78be1a8f14da0ab49ce1162348a5e&locations=3ba4ecdf4893100bc84aa7a3f1e46b98&locations=3ba4ecdf4893100bc84a8e6d38d46b70', 504, 540,
                    'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs',payload)
    lock.acquire()
    writeToExcel('Adobe Company', jobsDictionary, worksheet)
    lock.release()

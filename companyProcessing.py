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

def writeToExcel(title,jobsDictionary,worksheet,cell_format):
    global row
    row += 2
    worksheet.write(row, 0, title,cell_format)
    row += 1
    worksheet.write(row, 0, 'jobTitle',cell_format)
    worksheet.write(row, 1, 'jobId',cell_format)
    worksheet.write(row, 2, 'location',cell_format)
    worksheet.write(row, 3, 'postedOn',cell_format)
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

def qualcommComp(lock,worksheet,cell_format):
    payload = {
        "appliedFacets": {},
        "limit": 10,
        "offset": 0
    }
    jobsDictionary = initComp(tokenURL='https://qualcomm.wd5.myworkdayjobs.com/External',start=494,end=530,jobURL='https://qualcomm.wd5.myworkdayjobs.com/wday/cxs/qualcomm/External/jobs',payload=payload)
    lock.acquire()
    writeToExcel('Qualcomm Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def cienaComp(lock,worksheet,cell_format):
    payload = {
        "appliedFacets": {},
        "limit": 10,
        "offset": 0
    }
    jobsDictionary = initComp('https://ciena.wd5.myworkdayjobs.com/en-US/Careers',672,708,'https://ciena.wd5.myworkdayjobs.com/wday/cxs/ciena/Careers/jobs',payload)
    lock.acquire()
    writeToExcel('Ciena Company',jobsDictionary,worksheet,cell_format)
    lock.release()


def adobeComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{"jobFamilyGroup":["591af8b812fa10737af39db3d96eed9f"],"locationCountry":["c4f78be1a8f14da0ab49ce1162348a5e"],"locations":["3ba4ecdf4893100bc84aa7a3f1e46b98","3ba4ecdf4893100bc84a8e6d38d46b70"]},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp('https://adobe.wd5.myworkdayjobs.com/external_experienced?jobFamilyGroup=591af8b812fa10737af39db3d96eed9f&locationCountry=c4f78be1a8f14da0ab49ce1162348a5e&locations=3ba4ecdf4893100bc84aa7a3f1e46b98&locations=3ba4ecdf4893100bc84a8e6d38d46b70', 504, 540,
                    'https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs',payload)
    lock.acquire()
    writeToExcel('Adobe Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def paypalComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp(
        'https://paypal.wd1.myworkdayjobs.com/jobs',
        466, 502,
        'https://paypal.wd1.myworkdayjobs.com/wday/cxs/paypal/jobs/jobs', payload)
    lock.acquire()
    writeToExcel('Paypal Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def intelComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp(
        'https://intel.wd1.myworkdayjobs.com/External',
        472, 508,
        'https://intel.wd1.myworkdayjobs.com/wday/cxs/intel/External/jobs', payload)
    lock.acquire()
    writeToExcel('Intel Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def bakerhughesComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{"jobFamilyGroup":["5ec015e5642301a63ebe325f4b504d16"],"locationHierarchy1":["c4f78be1a8f14da0ab49ce1162348a5e"]},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp(
        'https://bakerhughes.wd5.myworkdayjobs.com/BakerHughes?jobFamilyGroup=5ec015e5642301a63ebe325f4b504d16&locationHierarchy1=c4f78be1a8f14da0ab49ce1162348a5e',
        671, 707,
        'https://bakerhughes.wd5.myworkdayjobs.com/wday/cxs/bakerhughes/BakerHughes/jobs', payload)
    lock.acquire()
    writeToExcel('Baker Hughes Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def yahooComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{"jobFamilyGroup":["91f14896cbbe0142bf25083fc74637b2","91f14896cbbe0150163e1d3fc7463fb2"]},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp(
        'https://ouryahoo.wd5.myworkdayjobs.com/careers?jobFamilyGroup=91f14896cbbe0142bf25083fc74637b2&jobFamilyGroup=91f14896cbbe0150163e1d3fc7463fb2',
        476, 512,
        'https://ouryahoo.wd5.myworkdayjobs.com/wday/cxs/ouryahoo/careers/jobs', payload)
    lock.acquire()
    writeToExcel('Yahoo Company', jobsDictionary, worksheet,cell_format)
    lock.release()

def mcafeeComp(lock,worksheet,cell_format):
    payload = {"appliedFacets":{},"limit":10,"offset":0,"searchText":""}
    jobsDictionary = initComp(
        'https://mcafee.wd1.myworkdayjobs.com/External/',474 ,510, 'https://mcafee.wd1.myworkdayjobs.com/wday/cxs/mcafee/External/jobs', payload)
    lock.acquire()
    writeToExcel('Mcafee Company', jobsDictionary, worksheet, cell_format)
    lock.release()
import requests
import bs4
import json
import threading

data = json.load(open('companiesData.json', 'r'))

row = 0


def initComp(tokenURL, jobURL, payload):
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

    jobsDictionary = {}
    jobsDictionary['full_stack'] = []
    jobsDictionary['back_end'] = []
    jobsDictionary['front_end'] = []
    jobsDictionary['tester'] = []

    for i in data['jobPostings']:
        if (i['postedOn'] == 'Posted 8 Days Ago' or i['postedOn'] == 'Posted 7 Days Ago' or i[
            'postedOn'] == 'Posted Today' or i[
            'postedOn'] == 'Posted Yesterday' or i['postedOn'] == 'Posted 6 Days Ago' or i[
            'postedOn'] == 'Posted 5 Days Ago' or i['postedOn'] == 'Posted 4 Days Ago' or i[
            'postedOn'] == 'Posted 3 Days Ago' or i['postedOn'] == 'Posted 2 Days Ago'):

            if(str(i['title']).lower().__contains__('tester') or str(i['title']).lower().__contains__('testing') or str(i['title']).lower().__contains__('tester') or str(i['title']).lower().__contains__('test') or str(i['title']).lower().__contains__('automation')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                   'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                jobsDictionary['tester'].append(Job)
            elif(str(i['title']).lower().__contains__('full stack') or str(i['title']).lower().__contains__('full-stack')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                   'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                jobsDictionary['full_stack'].append(Job)
            elif (str(i['title']).lower().__contains__('frontend') or str(i['title']).lower().__contains__('ui') or str(i['title']).lower().__contains__('ux')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                       'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                jobsDictionary['front_end'].append(Job)
            else:
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                       'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                jobsDictionary['back_end'].append(Job)

    # print(jobsDictionary)
    return jobsDictionary


def writeToExcel(title, jobsDictionary, worksheet, cell_format):
    global row
    worksheet.write(row, 0, str(title).upper(), cell_format)
    if (not jobsDictionary['full_stack']) and (not jobsDictionary['back_end']) and (not jobsDictionary['front_end']) and (not jobsDictionary['tester']):
        worksheet.write(row, 1, 'No Openings Found !!', cell_format)
        row += 2
        return
    startRow = row + 1
    if(jobsDictionary['full_stack']):
        row += 1
        worksheet.write(row, 0, 'Full Stack Roles', cell_format)
        row += 1
        worksheet.write(row, 0, 'Job Title', cell_format)
        worksheet.write(row, 1, 'Job Id', cell_format)
        worksheet.write(row, 2, 'Location', cell_format)
        worksheet.write(row, 3, 'Posted On', cell_format)
        worksheet.write(row, 4, 'Job Link', cell_format)
        row += 1
        # iterating through content list
        for item in jobsDictionary['full_stack']:
            column = 0
            for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                # write operation perform
                worksheet.write(row, column, item[i])
                column += 1
            # incrementing the value of row by one
            # with each iterations.
            row += 1
    if (jobsDictionary['back_end']):
        row += 1
        worksheet.write(row, 0, 'Back-End Roles', cell_format)
        row += 1
        worksheet.write(row, 0, 'Job Title', cell_format)
        worksheet.write(row, 1, 'Job Id', cell_format)
        worksheet.write(row, 2, 'Location', cell_format)
        worksheet.write(row, 3, 'Posted On', cell_format)
        worksheet.write(row, 4, 'Job Link', cell_format)
        row += 1
        # iterating through content list
        for item in jobsDictionary['back_end']:
            column = 0
            for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                # write operation perform
                worksheet.write(row, column, item[i])
                column += 1
            # incrementing the value of row by one
            # with each iterations.
            row += 1
    if (jobsDictionary['front_end']):
        row += 1
        worksheet.write(row, 0, 'Front-End Roles', cell_format)
        row += 1
        worksheet.write(row, 0, 'Job Title', cell_format)
        worksheet.write(row, 1, 'Job Id', cell_format)
        worksheet.write(row, 2, 'Location', cell_format)
        worksheet.write(row, 3, 'Posted On', cell_format)
        worksheet.write(row, 4, 'Job Link', cell_format)
        row += 1
        # iterating through content list
        for item in jobsDictionary['front_end']:
            column = 0
            for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                # write operation perform
                worksheet.write(row, column, item[i])
                column += 1
            # incrementing the value of row by one
            # with each iterations.
            row += 1
    if (jobsDictionary['tester']):
        row += 1
        worksheet.write(row, 0, 'Tester Roles', cell_format)
        row += 1
        worksheet.write(row, 0, 'Job Title', cell_format)
        worksheet.write(row, 1, 'Job Id', cell_format)
        worksheet.write(row, 2, 'Location', cell_format)
        worksheet.write(row, 3, 'Posted On', cell_format)
        worksheet.write(row, 4, 'Job Link', cell_format)
        row += 1
        # iterating through content list
        for item in jobsDictionary['tester']:
            column = 0
            for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                # write operation perform
                worksheet.write(row, column, item[i])
                column += 1
            # incrementing the value of row by one
            # with each iterations.
            row += 1
    endRow = row - 1
    worksheet.add_table(startRow,0,endRow,4, {'header_row': False})
    row += 2
def getCompanyData(companyName, lock, worksheet, cell_format):
    jobsDictionary = initComp(data['companies'][0][str(companyName)]['tokenURL'],
                              data['companies'][0][str(companyName)]['jobURL'],
                              data['companies'][0][str(companyName)]['payload'])
    lock.acquire()
    writeToExcel(companyName + ' Company', jobsDictionary, worksheet, cell_format)
    lock.release()
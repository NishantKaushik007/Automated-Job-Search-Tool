import requests
import bs4
import json
import threading

data = json.load(open('companiesData.json', 'r'))

fresher_worksheet_row = 0
experienced_worksheet_row = 0


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
    jobsDictionary['fresher'] = {}
    jobsDictionary['experienced'] = {}

    jobsDictionary['fresher']['full_stack'] = []
    jobsDictionary['fresher']['back_end'] = []
    jobsDictionary['fresher']['front_end'] = []
    jobsDictionary['fresher']['tester'] = []

    jobsDictionary['experienced']['full_stack'] = []
    jobsDictionary['experienced']['back_end'] = []
    jobsDictionary['experienced']['front_end'] = []
    jobsDictionary['experienced']['tester'] = []

    for i in data['jobPostings']:
        if (i['postedOn'] == 'Posted 8 Days Ago' or i['postedOn'] == 'Posted 7 Days Ago' or i[
            'postedOn'] == 'Posted Today' or i[
            'postedOn'] == 'Posted Yesterday' or i['postedOn'] == 'Posted 6 Days Ago' or i[
            'postedOn'] == 'Posted 5 Days Ago' or i['postedOn'] == 'Posted 4 Days Ago' or i[
            'postedOn'] == 'Posted 3 Days Ago' or i['postedOn'] == 'Posted 2 Days Ago'):

            if(str(i['title']).lower().__contains__('tester') or str(i['title']).lower().__contains__('testing') or str(i['title']).lower().__contains__('tester') or str(i['title']).lower().__contains__('test') or str(i['title']).lower().__contains__('automation')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                   'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                if(str(i['title']).lower().__contains__('senior') or str(i['title']).lower().__contains__('engineer 4') or str(i['title']).lower().__contains__('engineer 3') or str(i['title']).lower().__contains__('sr.') or str(i['title']).lower().__contains__('lead') or str(i['title']).lower().__contains__('manager')):
                    jobsDictionary['experienced']['tester'].append(Job)
                else:
                    jobsDictionary['fresher']['tester'].append(Job)
            elif(str(i['title']).lower().__contains__('full stack') or str(i['title']).lower().__contains__('full-stack')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                   'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                if(str(i['title']).lower().__contains__('senior') or str(i['title']).lower().__contains__('engineer 4') or str(i['title']).lower().__contains__('engineer 3') or str(i['title']).lower().__contains__('sr.') or str(i['title']).lower().__contains__('lead') or str(i['title']).lower().__contains__('manager')):
                    jobsDictionary['experienced']['full_stack'].append(Job)
                else:
                    jobsDictionary['fresher']['full_stack'].append(Job)
            elif (str(i['title']).lower().__contains__('frontend') or str(i['title']).lower().__contains__('ui') or str(i['title']).lower().__contains__('ux')):
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                       'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                if(str(i['title']).lower().__contains__('senior') or str(i['title']).lower().__contains__('engineer 4') or str(i['title']).lower().__contains__('engineer 3') or str(i['title']).lower().__contains__('sr.') or str(i['title']).lower().__contains__('lead') or str(i['title']).lower().__contains__('manager')):
                    jobsDictionary['experienced']['front_end'].append(Job)
                else:
                    jobsDictionary['fresher']['front_end'].append(Job)
            else:
                Job = {'jobTitle': i['title'], 'jobId': i['bulletFields'][0], 'location': i['locationsText'],
                       'postedOn': i['postedOn'], 'jobLink': tokenURL + i['externalPath']}
                if(str(i['title']).lower().__contains__('senior') or str(i['title']).lower().__contains__('engineer 4') or str(i['title']).lower().__contains__('engineer 3') or str(i['title']).lower().__contains__('sr.') or str(i['title']).lower().__contains__('lead') or str(i['title']).lower().__contains__('manager')):
                    jobsDictionary['experienced']['back_end'].append(Job)
                else:
                    jobsDictionary['fresher']['back_end'].append(Job)

    # print(jobsDictionary)
    return jobsDictionary


def writeToExcel(title, jobsDictionary, fresher_worksheet, experienced_worksheet, cell_format):
    global fresher_worksheet_row
    global experienced_worksheet_row
    fresher_worksheet.write(fresher_worksheet_row, 0, str(title).upper(), cell_format)
    experienced_worksheet.write(experienced_worksheet_row, 0, str(title).upper(), cell_format)
    if (not jobsDictionary['fresher']['full_stack']) and (not jobsDictionary['fresher']['back_end']) and (not jobsDictionary['fresher']['front_end']) and (not jobsDictionary['fresher']['tester']):
        fresher_worksheet.write(fresher_worksheet_row, 1, 'No Openings Found !!', cell_format)
        fresher_worksheet_row += 2
    else:
        fresher_startRow = fresher_worksheet_row + 1
        if (jobsDictionary['fresher']['full_stack']):
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Full Stack Roles', cell_format)
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Job Title', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 1, 'Job Id', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 2, 'Location', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 3, 'Posted On', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 4, 'Job Link', cell_format)
            fresher_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['fresher']['full_stack']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    fresher_worksheet.write(fresher_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                fresher_worksheet_row += 1
        if (jobsDictionary['fresher']['back_end']):
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Back-End Roles', cell_format)
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Job Title', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 1, 'Job Id', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 2, 'Location', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 3, 'Posted On', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 4, 'Job Link', cell_format)
            fresher_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['fresher']['back_end']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    fresher_worksheet.write(fresher_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                fresher_worksheet_row += 1
        if (jobsDictionary['fresher']['front_end']):
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Front-End Roles', cell_format)
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Job Title', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 1, 'Job Id', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 2, 'Location', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 3, 'Posted On', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 4, 'Job Link', cell_format)
            fresher_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['fresher']['front_end']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    fresher_worksheet.write(fresher_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                fresher_worksheet_row += 1
        if (jobsDictionary['fresher']['tester']):
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Tester Roles', cell_format)
            fresher_worksheet_row += 1
            fresher_worksheet.write(fresher_worksheet_row, 0, 'Job Title', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 1, 'Job Id', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 2, 'Location', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 3, 'Posted On', cell_format)
            fresher_worksheet.write(fresher_worksheet_row, 4, 'Job Link', cell_format)
            fresher_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['fresher']['tester']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    fresher_worksheet.write(fresher_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                fresher_worksheet_row += 1
        fresher_endRow = fresher_worksheet_row - 1
        fresher_worksheet.add_table(fresher_startRow, 0, fresher_endRow, 4, {'header_row': False})
        fresher_worksheet_row += 2

    if (not jobsDictionary['experienced']['full_stack']) and (not jobsDictionary['experienced']['back_end']) and (not jobsDictionary['experienced']['front_end']) and (not jobsDictionary['experienced']['tester']):
        experienced_worksheet.write(experienced_worksheet_row, 1, 'No Openings Found !!', cell_format)
        experienced_worksheet_row += 2
    else:
        experienced_startRow = experienced_worksheet_row + 1
        if (jobsDictionary['experienced']['full_stack']):
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Full Stack Roles', cell_format)
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Job Title', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 1, 'Job Id', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 2, 'Location', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 3, 'Posted On', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 4, 'Job Link', cell_format)
            experienced_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['experienced']['full_stack']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    experienced_worksheet.write(experienced_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                experienced_worksheet_row += 1
        if (jobsDictionary['experienced']['back_end']):
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Back-End Roles', cell_format)
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Job Title', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 1, 'Job Id', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 2, 'Location', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 3, 'Posted On', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 4, 'Job Link', cell_format)
            experienced_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['experienced']['back_end']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    experienced_worksheet.write(experienced_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                experienced_worksheet_row += 1
        if (jobsDictionary['experienced']['front_end']):
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Front-End Roles', cell_format)
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Job Title', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 1, 'Job Id', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 2, 'Location', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 3, 'Posted On', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 4, 'Job Link', cell_format)
            experienced_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['experienced']['front_end']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    experienced_worksheet.write(experienced_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                experienced_worksheet_row += 1
        if (jobsDictionary['experienced']['tester']):
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Tester Roles', cell_format)
            experienced_worksheet_row += 1
            experienced_worksheet.write(experienced_worksheet_row, 0, 'Job Title', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 1, 'Job Id', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 2, 'Location', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 3, 'Posted On', cell_format)
            experienced_worksheet.write(experienced_worksheet_row, 4, 'Job Link', cell_format)
            experienced_worksheet_row += 1
            # iterating through content list
            for item in jobsDictionary['experienced']['tester']:
                column = 0
                for i in ['jobTitle', 'jobId', 'location', 'postedOn', 'jobLink']:
                    # write operation perform
                    experienced_worksheet.write(experienced_worksheet_row, column, item[i])
                    column += 1
                # incrementing the value of row by one
                # with each iterations.
                experienced_worksheet_row += 1
        experienced_endRow = experienced_worksheet_row - 1
        experienced_worksheet.add_table(experienced_startRow, 0, experienced_endRow, 4, {'header_row': False})
        experienced_worksheet_row += 2
    
def getCompanyData(companyName, lock, fresher_worksheet, experienced_worksheet, cell_format):
    jobsDictionary = initComp(data['companies'][0][str(companyName)]['tokenURL'],
                              data['companies'][0][str(companyName)]['jobURL'],
                              data['companies'][0][str(companyName)]['payload'])
    lock.acquire()
    writeToExcel(companyName + ' Company', jobsDictionary, fresher_worksheet, experienced_worksheet, cell_format)
    lock.release()
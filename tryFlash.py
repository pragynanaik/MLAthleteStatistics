from requests import get
from contextlib import closing
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
 
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
import csv 
import os
import ssl
import urllib
import time
import json



# Checks to see if a given url points to a valid website 
def good_response(resp):
    contentType = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and contentType is not None and contentType.find('html') > -1)

# Returns the content of an html page (if Valid)
def simple_get(url):
    with closing(get(url)) as resp: 
        if good_response(resp):
            return resp.content
        else:
            return None


# Takes in the user inputted value that specifies whether the user wants to store all the matches for a given date or a date range. 
# Stores the match information in match.csv 
def entire_document(yearSeason):


    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })
    
    browser = webdriver.Chrome(chrome_options=option, executable_path='/Users/pragynanaik/Desktop/MLAthleteStatistics/selenium/webdriver/chrome/chromedriver')

    browser.get("https://www.ultimatetennisstatistics.com/season?season=" + yearSeason)

    cookies = browser.find_element_by_css_selector('#cookiesNotification button')
    cookies.click()

    events = browser.find_element_by_id("eventsPill")
    events.click()

    
    time.sleep(4)
    urlSeason = browser.page_source
    soup = BeautifulSoup(urlSeason, 'html.parser')

    seasonTable = soup.find(id='seasonEventsTable')

    allPageIds = seasonTable.find('tbody').find_all("a")

    allIds = []
    for id in allPageIds:
        if 'tournament' in id['href']:
            allIds.append(id['href'])
    
    footer = soup.find(id='seasonEventsTable-footer')
    nexts = footer.select('li.next.disabled')
 
    print("first page")
    i = 0

    while (len(nexts) == 0): 
        i += 1
        print("next page: " + str(i))

        nextButton = browser.find_element_by_css_selector('.next a')
        nextButton.click()
        
        time.sleep(4)
        
        urlSeason = browser.page_source

        soup = BeautifulSoup(urlSeason, 'html.parser')

        seasonTable = soup.find(id='seasonEventsTable')
        

        allPageIds = seasonTable.find('tbody').find_all("a")


        for id in allPageIds:
            if 'tournament' in id['href']:
                allIds.append(id['href'])
        
        
        
        footer = soup.find(id='seasonEventsTable-footer')
        nexts = footer.select('li.next.disabled')
       
        

    print(allIds)

    with open('match.csv', mode='w') as match_file:
        filename = os.path.join(os.path.dirname(__file__), 'match.csv');
        match_writer = csv.writer(match_file, delimiter=',', quotechar='"')
        match_writer.writerow(['Match Date', 'Player 1 Name', 'Player 2 Name', 'Score', 'Winning player name', 'Player 1 Ranking', 'Player 2 Ranking', 
        'Player 1 Aces', 'Player 2 Aces', 'Player 1 Double Faults', 'Player 2 Double Faults', 'Player 1 1st Serve Percentage', 'Player 2 1st Serve Percentage',
        'Player 1 1st Serve Points Won', 'Player 2 1st Serve Points Won', 'Player 1 2nd Serve Points Won', 'Player 2 2nd Serve Points Won', 
        'Player 1 Break Points Saved', 'Player 2 Break Points Saved', 'Player 1 Return', 'Player 2 Return', 'Player 1 1st Return Points Won', 
        'Player 2 1st Return Points Won', 'Player 1 2nd Return Points Won', 'Player 2 2nd Return Points Won', 'Player 1 Break Points Converted',
        'Player 2 Break Points Converted', 'Player 1 Winners', 'Player 2 Winners', 'Player 1 Unforced Errors', 'Player 2 Unforced Errors', 'Player 1 Net Points Won',
        'Player 2 Net Points Won', 'Player 1 Max Points in Row', 'Player 2 Max Points in Row', 'Player 1 Service Points Won', 'Player 2 Service Points Won',
        'Player 1 Return Points Won', 'Player 2 Return Points Won', 'Player 1 Total Points Won', 'Player 2 Total Points Won', 'Player 1 Max Games in Row', 
        'Player 2 Max Games in Row', 'Player 1 Service Games Won', 'Player 2 Service Games Won', 'Player 1 Return Games Won', 'Player 2 Return Games Won', 
        'Player 1 Total Games Won', 'Player 2 Total Games Won', 'Player 1 Distance Covered', 'Player 2 Distance Covered'])

        for idValue in allIds: 
        # idValue = '/tournamentEvent?tournamentEventId=3163'
            create_csv_table(match_writer, idValue)

        

# writes to an inputted csv file writer, information concerning matches based on an inputted year, month, and day 
def create_csv_table(writer, idValue):

    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 1 
    })


    browser = webdriver.Chrome(chrome_options=option, executable_path='/Users/pragynanaik/Desktop/MLAthleteStatistics/selenium/webdriver/chrome/chromedriver')
    browser.get("https://www.ultimatetennisstatistics.com" + idValue)
    cookies = browser.find_element_by_css_selector('#cookiesNotification button')
    cookies.click()

    initialBrowser = browser.page_source
    initialSoup = BeautifulSoup(initialBrowser, 'html.parser')
    
    matches = []
    bigDiv = initialSoup.find('div', attrs={'class':'col-md-2'})
    info = bigDiv.find_all('td')
    dateOfMatch = info[2].text

    resultsTable = initialSoup.find(id="resultsTable")
    eachMatch = resultsTable.find_all('table', attrs={'class': 'table-bordered'})
    ids = []
    
    for match in eachMatch:
        allStats = match.find_all('td', attrs={'class': 'stats'})
        if (len(allStats) == 0 or allStats == None):
            ids.append("")
        else: 
            if (allStats[0].find('a') is not None):
                ids.append(allStats[0].find('a').get('id'))

    totalMatches = len(ids)

    for matchVal in range(totalMatches):
        idVal = ids[matchVal]
  
        if (idVal != ''): 
            statistics = browser.find_element_by_id(idVal)
            if(statistics.is_displayed()):
                if (idVal != 'matchStats-139048'):
                    statistics.click()
                    time.sleep(4)
            else:
                idVal = ''

        browserURL = browser.page_source

        soup = BeautifulSoup(browserURL, 'html.parser')
        matchId = idVal

        resultsTable = soup.find(id="resultsTable")
        eachMatch = resultsTable.find_all('table', attrs={'class': 'table-bordered'})
        i = eachMatch[matchVal]

        matchInfo = [dateOfMatch, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '']
        wonMatch = 0
        player = 0
        players = []

        rows = i.find_all('td', attrs={'class': 'player'})
        for j in rows: 
            player = player + 1
            winner = j.find_all('strong')
            if (len(winner) == 1):
                wonMatch = player
        

            players.append(j.find('a').text)

        allRows = i.find_all('tr')
        score1 = []
        score2 = []
        for p in range(2):
            allTD = allRows[p].find_all('td', attrs={'class': 'score'})
            if p == 0:
                for k in allTD:
                    if (len(k.text) == 0): 
                        score1.append('')
                    else: 
                        score1.append(k.text[0])
            else:
                for k in allTD: 
                    if (len(k.text) == 0): 
                        score2.append('')
                    else: 
                        score2.append(k.text[0])
        
        totalScore = ''
        for a in range(len(score1) - 1):
            totalScore = totalScore + "(" + score1[a] + '-' + score2[a] + ')' 
        
        matchInfo[1] = players[0]
        matchInfo[2] = players[1]
        matchInfo[3] = totalScore
        matchInfo[4] = players[wonMatch - 1]

        # statsTD = eachMatch.find('td', attrs={'class': 'stats'})

        if (idVal != ''):
            otherData = i.find('div', attrs={'id': matchId + 'Overview'})
            print(idVal)
            if (otherData is not None):
                overviewRows = otherData.find_all('tr')

                acePerc = overviewRows[1].find_all('th')
                matchInfo[7] = acePerc[0].text
                matchInfo[8] = acePerc[3].text

                doubleFault = overviewRows[2].find_all('th')
                matchInfo[9] = doubleFault[0].text
                matchInfo[10] = doubleFault[3].text

                firstServePerc = overviewRows[3].find_all('th')
                matchInfo[11] = firstServePerc[0].text
                matchInfo[12] = firstServePerc[3].text

                firstServeWon = overviewRows[4].find_all('th')
                matchInfo[13] = firstServeWon[0].text
                matchInfo[14] = firstServeWon[3].text

                secondServeWon = overviewRows[5].find_all('th')
                matchInfo[15] = secondServeWon[0].text
                matchInfo[16] = secondServeWon[3].text

                breakPoints = overviewRows[6].find_all('th')
                matchInfo[17] = breakPoints[0].text
                matchInfo[18] = breakPoints[3].text

                firstReturnWon = overviewRows[9].find_all('th')
                matchInfo[21] = firstReturnWon[0].text
                matchInfo[22] = firstReturnWon[3].text

                secondReturnWon = overviewRows[10].find_all('th')
                matchInfo[23] = secondReturnWon[0].text
                matchInfo[24] = secondReturnWon[3].text

                servicePoints = overviewRows[7].find_all('th')
                matchInfo[35] = servicePoints[0].text
                matchInfo[36] = servicePoints[3].text

                returnPoints = overviewRows[12].find_all('th')
                matchInfo[37] = returnPoints[0].text
                matchInfo[38] = returnPoints[3].text

                totalPoints = overviewRows[15].find_all('th')
                matchInfo[39] = totalPoints[0].text
                matchInfo[40] = totalPoints[3].text

                serveData = i.find('div', attrs={'id': matchId + 'Serve'})
                serveRows = serveData.find_all('tr')

                serviceGames = serveRows[15].find_all('th')
                matchInfo[43] = serviceGames[0].text
                matchInfo[44] = serviceGames[3].text

                returnData = i.find('div', attrs={'id': matchId + 'Return'})
                returnRows = returnData.find_all('tr')

                returnGames = returnRows[13].find_all('th')
                matchInfo[45] = returnGames[0].text
                matchInfo[46] = returnGames[3].text

                totalData = i.find('div', attrs={'id': matchId + 'Total'})
                totalRows = totalData.find_all('tr')

                totalGames = totalRows[7].find_all('th')
                matchInfo[47] = totalGames[0].text
                matchInfo[48] = totalGames[3].text

                statistics.click()

        matches.append(matchInfo)

    print(idValue)

    browser.close()
    for match in matches:
        writer.writerow(match)


# entire_document('2008')



    

    

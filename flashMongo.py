import pymongo
from pymongo import MongoClient
import datetime
import csv
from tryFlash import entire_document


client = MongoClient("mongodb+srv://Pragyna:NavyBlue2016@mlathletedataset.lhiuy.mongodb.net/AthleteData?retryWrites=true&w=majority")
db = client.dataStatistics 
rangeBoolean = input("Which year would you like to add to the database?")

allYear = db['season' + rangeBoolean]
entire_document(rangeBoolean)

with open('match.csv') as csvfile:
    readCsv = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in readCsv:
        count += 1;
        personDocument = {
            'Match Date': row[0], 'Player 1 Name': row[1], 'Player 2 Name': row[2], 'Score': row[3], 'Winning player name': row[4], 'Player 1 Ranking': row[5], 'Player 2 Ranking': row[6], 
        'Player 1 Aces': row[7], 'Player 2 Aces': row[8], 'Player 1 Double Faults': row[9], 'Player 2 Double Faults': row[10], 'Player 1 1st Serve Percentage': row[11], 'Player 2 1st Serve Percentage': row[12],
        'Player 1 1st Serve Points Won': row[13], 'Player 2 1st Serve Points Won': row[14], 'Player 1 2nd Serve Points Won': row[15], 'Player 2 2nd Serve Points Won': row[16], 
        'Player 1 Break Points Saved': row[17], 'Player 2 Break Points Saved': row[18], 'Player 1 Return': row[19], 'Player 2 Return': row[20], 'Player 1 1st Return Points Won': row[21], 
        'Player 2 1st Return Points Won': row[22], 'Player 1 2nd Return Points Won': row[23], 'Player 2 2nd Return Points Won': row[24], 'Player 1 Break Points Converted': row[25],
        'Player 2 Break Points Converted': row[26], 'Player 1 Winners': row[27], 'Player 2 Winners': row[28], 'Player 1 Unforced Errors': row[29], 'Player 2 Unforced Errors': row[30], 'Player 1 Net Points Won': row[31],
        'Player 2 Net Points Won': row[32], 'Player 1 Max Points in Row': row[33], 'Player 2 Max Points in Row': row[34], 'Player 1 Service Points Won': row[35], 'Player 2 Service Points Won': row[36],
        'Player 1 Return Points Won': row[37], 'Player 2 Return Points Won': row[38], 'Player 1 Total Points Won': row[39], 'Player 2 Total Points Won': row[40], 'Player 1 Max Games in Row': row[41], 
        'Player 2 Max Games in Row': row[42], 'Player 1 Service Games Won': row[43], 'Player 2 Service Games Won': row[44], 'Player 1 Return Games Won': row[45], 'Player 2 Return Games Won': row[46], 
        'Player 1 Total Games Won': row[47], 'Player 2 Total Games Won': row[48], 'Player 1 Distance Covered': row[49], 'Player 2 Distance Covered': row[50]
        }  

        allYear.insert_one(personDocument)   

    print(count)
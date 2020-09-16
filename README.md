# MLAthleteDatasets

The ML Athlete Datasets script takes in an inputted year and adds the data from that year's match statistics onto the dataStatistics database on MongoDB.

The scraping is done on the following website:

  [Tennis Match Statistics](https://www.ultimatetennisstatistics.com/tournamentEvents)

It uses this ordering for which data values are inputted:

  [DataSet Column Values](https://docs.google.com/spreadsheets/d/1ki_dzgo0zqaZXxItSEQC-4jddFkN937YUbjdx81rQCk/edit?usp=sharing)


This script takes in a date value and creates a csv file `match.csv` that takes all the data from that year and puts it into a csv format. It then connects to MongoDB and uploads the data.

To run the script, you need to run flashMongo.py in python, where you will be asked to input a **single year**.



### Outputs

    Keep in mind that the program does run slow. In order to track progress, the program
    prints out the initial list of tournament ids from that year as well as which
    current tournament id is associated with the current webpage being scraped. Additionally,
    it prints out which specific match on the page is being scraped.

### Packages

    This can run on python 3 version. This requires the following packages to be installed:
        Beautiful Soup
        Requests

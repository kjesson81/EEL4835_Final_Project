import requests
import json
from bs4 import BeautifulSoup

# write data function
def write_data(database, filename):
    with open(filename, "a") as f:
        f.write(database)

# create empty dictionary
synonymsDict = {}
synonym_history = []

# loop will allow for multiple words to be input
loop = True
while loop is True:

    # opens historical database for synonyms
    with open("synonymsDB.json", "r") as data:
        historicalDB = json.load(data)

    user_input = input("Please enter a word:").lower()
    # will check to see if input word has already been historized and will not access web if it has been
    if user_input.lower() in historicalDB.keys():
        print(user_input + " has already been entered. The synonyms are:\n")
        for word in historicalDB.pop(user_input):
            print(word)

    else:
        # Start of web-scraping code
        html_text = requests.get(f'https://www.thesaurus.com/browse/{user_input}').text
        soup = BeautifulSoup(html_text, 'lxml')
        synonym_combined = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')

        print("The synonyms for " + user_input + " are:")
        for synonym in synonym_combined:
            print(synonym.text)
            synonym_history.append(synonym.text)

        # formatting the data pulled from website
        synonymsDict[user_input] = synonym_history      # creates key-value pair in the dictionary format
        synonym_history = []        # clears the synonyms for the current input word to be used again in while loop

        # writes data to the JSON file
        with open("synonymsDB.json", "w") as write_data:
            json.dump(synonymsDict, write_data, indent=4)

    # just a script for testing for multiple input. Will need to be refined for final submission
    try_again = input("Do you want to try another word? Input yes or no.\n")
    if try_again == "no" or 'N' or 'n' or "No":
        loop = False
    if try_again == "yes" or 'Y' or 'y' or "Yes":
        loop = True

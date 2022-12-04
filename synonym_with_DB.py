import requests
import json
import time
import schedule
from bs4 import BeautifulSoup
from os.path import exists


def web_scraper(word):
    html_text = requests.get(f'https://www.thesaurus.com/browse/{word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    synonyms = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')
    return synonyms


# create empty dictionary
synonyms_dict = {}
input_synonyms = []
cont = True

while cont:

    if exists("synonymsDB.json"):
        # opens historical database for synonyms
        with open("synonymsDB.json", "r") as data:
            synonym_history = json.load(data)

        # obtains user input
        user_input = input("Please enter a word:").lower().strip()

        # check to see if input word is in historical dictionary
        if user_input in synonym_history.keys():
            print(user_input + " has already been entered. The synonyms are:\n")
            for existing_word in synonym_history.pop(user_input):
                print(existing_word)

        else:
            synonyms_list = web_scraper(user_input)

            print("The synonyms for " + user_input + " are:")
            for synonym in synonyms_list:
                print(synonym.text)
                input_synonyms.append(synonym.text)

            # formatting the data in dictionary format and removing additional spaces
            synonyms_dict[user_input] = [word.strip() for word in input_synonyms]

            input_synonyms = []     # clears the synonyms to re-run code

            # writes data to the JSON file
            with open("synonymsDB.json", "w") as file:
                json.dump(synonyms_dict, file, indent=4)

        repeat = input("do you wish to continue?").lower()
        if repeat == "n":
            cont = False

        # check for new updates

    else:
        file = open("synonymsDB.json", "w")
        empty_dict = {}
        json.dump(empty_dict, file)
        file.close()

# with open("synonymsDB.json", "r") as data:
#     synonym_history = json.load(data)
# 
# for word in synonym_history.keys():
#     schedule.every().day.at("23:59").do(web_scraper(word))
#     

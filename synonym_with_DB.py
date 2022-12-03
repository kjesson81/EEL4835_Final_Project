import requests
import json
from bs4 import BeautifulSoup

# create empty dictionary
synonyms_dict = {}
input_synonyms = []
cont = True

while cont:

    # opens historical database for synonyms
    with open("synonymsDB.json", "r") as data:
        synonym_history = json.load(data)

    # obtains user input
    user_input = input("Please enter a word:").lower().strip()

    # will check to see if input word has already been historized and will not access web if it has been
    if user_input in synonym_history.keys():
        print(user_input + " has already been entered. The synonyms are:\n")
        for existing_word in synonym_history.pop(user_input):
            print(existing_word)

    else:
        # Start of web-scraping code
        html_text = requests.get(f'https://www.thesaurus.com/browse/{user_input}').text
        soup = BeautifulSoup(html_text, 'lxml')
        synonyms_list = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')

        print("The synonyms for " + user_input + " are:")
        for synonym in synonyms_list:
            print(synonym.text)
            # input_synonyms.append('"' + synonym.text + '"')
            input_synonyms.append(synonym.text)

        # formatting the data pulled from website
        synonyms_dict[user_input] = [word.strip() for word in input_synonyms]      # creates key-value pair in the dictionary format
        input_synonyms = []        # clears the synonyms for the current input word to be used again in while loop

        # writes data to the JSON file
        with open("synonymsDB.json", "w") as file:
            json.dump(synonyms_dict, file, indent=4)

    repeat = input("do you wish to continue?").lower()
    if repeat == "n":
        cont = False

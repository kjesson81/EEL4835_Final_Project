import requests
import json
from bs4 import BeautifulSoup
from os.path import exists


def get_synonyms_from_web(word):
    synonyms = []
    html_text = requests.get(f'https://www.thesaurus.com/browse/{word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    synonyms_from_web = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')
   
    for synonym in synonyms_from_web:
        print(synonym.text)
        synonyms.append(synonym.text)
    synonyms_result = [word.strip() for word in synonyms]

    if not synonyms_result:
        synonyms_result = [ word + " was not found. Either it is not in thesaurus.com, or the word does not exist"]
        print(synonyms_result[0])
    
    return synonyms_result


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
            synonyms_dict[user_input] = get_synonyms_from_web(user_input)

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

import requests
import json
from bs4 import BeautifulSoup
from os.path import exists

synonyms_dict = {}

def get_synonyms_from_web(word):
    synonyms = []
    html_text = requests.get(f'https://www.thesaurus.com/browse/{word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    synonyms_from_web = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')

    print("The synonyms for " + word + " are:")
    for synonym in synonyms_from_web:
        print(synonym.text)
        synonyms.append(synonym.text)
    print('\n')
    synonyms_result = [word.strip() for word in synonyms]

    if not synonyms_result:
        synonyms_result = [word + " was not found. Either it is not in thesaurus.com, or the word does not exist"]
        print(synonyms_result[0])
    return synonyms_result


def synonyms(word):

    if exists("synonymsDB.json"):
        # opens historical database for synonyms
        with open("synonymsDB.json", "r") as data:
            synonym_history = json.load(data)

        # obtains user input
        user_input = word.lower().strip()

        # check to see if input word is in historical dictionary
        if user_input in synonym_history.keys():
            existing_words = []
            print(user_input + " has already been entered. The synonyms are:")
            for existing_word in synonym_history.pop(user_input):
                print(existing_word)
                existing_words.append(existing_word)
            synonyms_dict.setdefault(user_input, existing_words)
            print('\n')
        else:
            synonyms_dict.setdefault(user_input, get_synonyms_from_web(user_input))

            # writes data to the JSON file
            with open("synonymsDB.json", "w") as file:
                json.dump(synonyms_dict, file, indent=4)

    else:
        f = open("synonymsDB.json", "w")
        json.dump("{}", f)
        f.close()

    return synonyms_dict


run_code = input("Enter '1' if you want to type in your own words, and enter '2' if you want to read words from a file.\n")

if run_code == '1':
    user_input = input("Please enter a word to find it's synonyms!\n")
    synonyms(user_input)
elif run_code == '2':
    filename = input("Please enter the name of the file with words in it.\n")
    if exists(filename):
        with open(filename, "r") as input_file:
            input_words = input_file.readlines()

        write_data = []
        output_file = open("output.json", "w")
        for word in input_words:
            write_data.append(synonyms(word))
        length = len(write_data)
        json.dump(write_data[length-1], output_file, indent=4)
        output_file.close()
        print("Synonyms have been written to a file called 'output.json'")
else:
    print("You entered an invalid input. Goodbye.")

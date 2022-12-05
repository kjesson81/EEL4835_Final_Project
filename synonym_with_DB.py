#!/usr/bin/python3
import requests
import schedule
import time
import json
import time
import schedule
from bs4 import BeautifulSoup
from os.path import exists

synonyms_dict = {}


def get_synonyms_from_web(word):
    synonyms = []
    html_text = requests.get(f'https://www.thesaurus.com/browse/{word}').text
    soup = BeautifulSoup(html_text, 'lxml')
    div = soup.find("div", attrs={"data-testid": "word-grid-container"})
    synonyms_from_web = soup.find_all('a', class_="css-ixatld e15rdun50")

    for li in div.find_all("li"):
        link = li.find("a")
        if link:
            text = link.text.strip()
            synonyms.append(text)

    if not synonyms:
        synonyms = [word + " was not found. Either it is not in thesaurus.com, or the word does not exist"]
        print(synonyms[0])
    return synonyms


def synonyms(word):
    if exists("synonymsDB.json"):
        # opens historical database for synonyms
        with open("synonymsDB.json", "r") as data:
            synonyms_dict = json.load(data)

        # obtains user input
        user_input = word.lower().strip()

        # check to see if input word is in historical dictionary
        if user_input in synonyms_dict.keys():
            existing_words = []
            print(user_input + " has already been entered. The synonyms are:")
            for value in synonyms_dict.setdefault(user_input):
                print(value)

        else:
            synonyms_dict.setdefault(user_input, get_synonyms_from_web(user_input))
            for value in synonyms_dict.setdefault(user_input):
                print(value)
            # writes data to the JSON file
            with open("synonymsDB.json", "w") as file:
                json.dump(synonyms_dict, file, indent=4)

    else:
        f = open("synonymsDB.json", "w")
        json.dump({}, f)
        f.close()

    return synonyms_dict


run_code = input(
    "Enter '1' if you want to type in your own words, and enter '2' if you want to read words from a file.\n")

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
        json.dump(write_data[length - 1], output_file, indent=4)
        output_file.close()
        print("Synonyms have been written to a file called 'output.json'")
else:
    print("You entered an invalid input. Goodbye.")

with open("synonymsDB.json", "r") as data:
    synonyms_dict = json.load(data)

if __name__ == '__main__':
    i = 0
    x = True
    while x:
        with open("synonymsDB.json", "r") as data:
            synonyms_dict = json.load(data)
        time_wait = 3
        time.sleep(time_wait)
        i += 1

        for existing_word in synonyms_dict.keys():
            existing_synonyms = synonyms_dict[existing_word]
            update = get_synonyms_from_web(existing_word)
            print("Checking for update...")
            if len(update) != len(existing_synonyms):
                update_flag = True
                synonyms_dict.setdefault(existing_word, update)
                with open("synonymsDB.json", "w") as file:
                    json.dump(synonyms_dict, file, indent=4)
            else:
                update_flag = False

            if update_flag:
                print("Updated synonyms for " + existing_word)
            else:
                print("no update needed for " + existing_word)

        if i == 5:
            x = False

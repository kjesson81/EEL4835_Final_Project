#!/usr/bin/python3
import requests
import json
import time
from bs4 import BeautifulSoup
from os.path import exists

synonyms_dict = {}

# this function will access thesaurus.com and use BeautifulSoup to extract the synonyms
def get_synonyms_from_web(word):
    synonyms = []
    html_text = requests.get(f'https://www.thesaurus.com/browse/{word}').text
    soup = BeautifulSoup(html_text, 'lxml')

    # this accesses the html grid container that the synonyms are in
    synonyms_grid = soup.find("div", attrs={"data-testid": "word-grid-container"})

    # the for loop will go into the grid container and extract data for each synonym that has a "li" element
    for li in synonyms_grid.find_all("li"):
        link = li.find("a")
        if link:
            text = link.text.strip()            # only extract the text from html code
            synonyms.append(text)               # add text to synonym list

    # if the word returns and empty array, let user know
    if not synonyms:
        synonyms = [word + " was not found. Either it is not in thesaurus.com, or the word does not exist"]
        print(synonyms[0])

    return synonyms


def synonyms(word):

    if exists("synonymsDB.json"):
        # opens historical database for synonyms if it exists
        with open("synonymsDB.json", "r") as data:
            synonyms_dict = json.load(data)

        # obtains user input
        user_input = word.lower().strip()

        # check to see if input word is in historical dictionary
        if user_input in synonyms_dict.keys():
            print(user_input + " has already been entered. The synonyms are:")
            for value in synonyms_dict.setdefault(user_input):
                print(value)
        else:
            # creates/updates key value pair and print synonyms.
            synonyms_dict.setdefault(user_input, get_synonyms_from_web(user_input))
            for value in synonyms_dict.setdefault(user_input):
                print(value)

            # writes data to the JSON file
            with open("synonymsDB.json", "w") as file:
                json.dump(synonyms_dict, file, indent=4)

    else:
        # creates an empty .json file if it does not exist
        f = open("synonymsDB.json", "w")
        json.dump({}, f)
        f.close()

    return synonyms_dict


run_code = input("Enter '1' if you want to type in words, and enter '2' if you want to read words from a file.\n")

if run_code == '1':
    user_input = input("Please enter a word to find it's synonyms!\n")
    synonyms(user_input)
elif run_code == '2':

    filename = input("Please enter the name of the file with words in it.\n")
    if exists(filename):
        # reads content of file
        with open(filename, "r") as input_file:
            words_from_file = input_file.readlines()

        write_data = []         # create empty array to store data to be written

        output_file = open("output.json", "w")
        for word in words_from_file:
            write_data.append(synonyms(word))    # calls synonyms function to get synonyms and store in write_data
        length = len(write_data)
        # writes data to output file
        json.dump(write_data[length - 1], output_file, indent=4)
        output_file.close()
        print("Synonyms have been written to a file called 'output.json'")
        
# NOTE: the words from the file are also updated in the synonymsDB.json file. 
# output.json is a separate file for only words in the file. 
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
            
            # checks to see if there was change in the amount of synonyms in the website and if so, re-run script 
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

        if i == 2:
            x = False

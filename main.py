import time

from bs4 import BeautifulSoup
import requests

user_input = input("Please enter a word:").lower()


# This line will go to the website and return the html text as the variable html_text.

def get_synonym():
    html_text = requests.get(f'https://www.thesaurus.com/browse/{user_input}').text

    soup = BeautifulSoup(html_text, 'lxml')

    synonym_combined = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a',
                                                                                         class_='css-1gyuw4i eh475bn0') + soup.find_all(
        'a', class_='css-1n6g4vv eh475bn0')

    for synonym in synonym_combined:
        print(synonym.text)


if __name__ == '__main__':
    while True:
        get_synonym()
        time_wait = 3
        print(f"Waiting {time_wait} minutes..")
        time.sleep(time_wait * 60)

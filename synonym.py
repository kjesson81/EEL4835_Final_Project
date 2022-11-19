from bs4 import BeautifulSoup
import requests

user_input = input("Please enter a word:")

# This line will go to the website and return the html text as the variable html_text.
html_text = requests.get(f'https://www.thesaurus.com/browse/{user_input}').text

soup = BeautifulSoup(html_text, 'lxml')

synonym_combined = soup.find_all('a', class_='css-1kg1yv8 eh475bn0') + soup.find_all('a', class_='css-1gyuw4i eh475bn0') + soup.find_all('a', class_='css-1n6g4vv eh475bn0')

for synonym in synonym_combined:
    print(synonym.text)

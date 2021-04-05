import requests
from bs4 import BeautifulSoup
from replacements import current_id_replacements, verse_replacements, synonyms_replacements, translation_replacements, purport_replacements
from pathlib import Path


_index = 1

url = f'https://vanisource.org/wiki/SB_1.1.{_index}'

_source = requests.get(url)

soup = BeautifulSoup(_source.content, 'html.parser')

current_id = str(soup.find("h1", {"id": "firstHeading"}))
current_id = current_id_replacements(current_id)

verse = str(soup.find("div", {"class":"verse"}))
verse = verse_replacements(verse)
verse_entry = [{"roman": verse, "isProse": False}]

synonyms = str(soup.find("div", {"class": "synonyms"}))
synonyms = synonyms_replacements(synonyms)

translation = str(soup.find("div", {"class":"translation"}))
translation = translation_replacements(translation)

purport = str(soup.find("div", {"class": "purport"}))
purport = purport_replacements(purport)
purport_paras = list(filter(None, list(purport.split('\n'))))
purport_entry = [{"type": "regular", "text": para} for para in purport_paras]



knowledge = {"page_id": current_id, "verse": verse_entry, "synonyms": synonyms, "translation": translation, "purport": purport_entry}


print(knowledge)
print(type(knowledge))

if Path(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json').is_file():
    with open(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json', 'w') as json_file:
        print(knowledge, file=json_file)
else:
    with open(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json', 'x') as json_file:
        print(knowledge, file=json_file)

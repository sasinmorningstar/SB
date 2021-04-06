import requests
import re
from bs4 import BeautifulSoup
from replacements import current_id_replacements, verse_replacements, synonyms_replacements, translation_replacements, purport_replacements
from pathlib import Path


def parser():
    url = f'https://vanisource.org/wiki/SB_1.1.{_index}'

    _source = requests.get(url)

    soup = BeautifulSoup(_source.content, 'html.parser')

    b_tags = soup.find_all("b")

    headers = str(b_tags[len(b_tags)-1])
    headers = headers.replace('<b>', '')
    headers = headers.replace('</b>', '')
    headers = list(headers.split('-'))
    
    pointers = []
    for header in headers:
        head = list(list(header.split('>'))[1].split('<'))[0]
        pointers.append(head)
    
    # print(headers)
    # print(pointers)

    current_id = str(soup.find("h1", {"id": "firstHeading"}))
    current_id = current_id_replacements(current_id)

    if _index==1:
        navigation = {"current_id": current_id, "previous_id": None, "next_id": pointers[0]}
    else:
        navigation = {"current_id": current_id, "previous_id": pointers[0], "next_id": pointers[1]}

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



    knowledge = {"page_info": navigation, "verse": verse_entry, "synonyms": synonyms, "translation": translation, "purport": purport_entry}


    print(knowledge)
    print(type(knowledge))

    if Path(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json').is_file():
        with open(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json', 'w') as json_file:
            print(knowledge, file=json_file)
    else:
        with open(f'/home/somit/Projects/web-scraping/SB/1/1/{_index}.json', 'x') as json_file:
            print(knowledge, file=json_file)

for _index in range(1,24):
    parser()
import requests
import json
from bs4 import BeautifulSoup
from replacements import current_id_replacements, verse_replacements, synonyms_replacements, translation_replacements, purport_para_replacements, purport_verse_replacements
from pathlib import Path




def parser():
    global _index
    url = f'https://vanisource.org/wiki/SB_1.{chapter}.{_index}'

    _source = requests.get(url)

    soup = BeautifulSoup(_source.content, 'html.parser')
    
    b_tags = soup.find_all("b")

    headers = str(b_tags[len(b_tags)-1])
    headers = headers.replace('<b>', '')
    headers = headers.replace('</b>', '')
    headers = headers.replace(' - ', '---')
    headers = list(headers.split('---'))
    
    
    # Debug objects
    # print(headers)

    pointers = []
    for header in headers:
        head = list(list(header.split('>'))[1].split('<'))[0]
        pointers.append(head)
    
    print(pointers)

    current_id = str(soup.find("h1", {"id": "firstHeading"}))
    current_id = current_id_replacements(current_id)

    print(current_id)
    if len(current_id)>9 and current_id[7]=='.':
        _index = current_id[8:]
    elif len(current_id)>9:
        _index = current_id[7:]

    
    if len(pointers)==1:
        navigation = {"current_id": current_id, "previous_id": None, "next_id": pointers[0]}
    else:
        navigation = {"current_id": current_id, "previous_id": pointers[0], "next_id": pointers[1]}


    # Preparing Verse Entry
    verse = str(soup.find("div", {"class":"verse"}))
    verse = verse_replacements(verse)
    verse_entries = list(filter(None, list(verse.split('---'))))
    verse_entry = [{"roman": verse} for verse in verse_entries]
    verse_entry = verse_entry[1:]

    # Preparing Synonyms Entry
    synonyms = str(soup.find("div", {"class": "synonyms"}))
    synonyms = synonyms_replacements(synonyms)


    # Preparing Translation Entry
    translation = str(soup.find("div", {"class":"translation"}))
    translation = translation_replacements(translation)


    # Preparing Purport Entry
    purport = soup.find("div", {"class": "purport"})
   
    if purport:
        purport_para = str(purport.find_all("p"))
        purport_para = purport_para_replacements(purport_para)
        purport_paras = list(filter(None, list(purport_para.split('\n'))))

        # Preparing Purport Verse Entry.
        purport_verse = str(purport.find("dl"))
        purport_verse = purport_verse_replacements(purport_verse)
        purport_verses = list(filter(None, list(purport_verse.split('---'))))
    
        # Preparing a consolidated Purport Entry.
        purport_paras_list = [{"type": "regular", "text": para} for para in purport_paras]
    
        purport_verse_list = [{"type": "verse", "text": p_verse} for p_verse in purport_verses]

        if str(None) not in purport_verses:
            purport_entry = purport_paras_list + purport_verse_list
        else:
            purport_entry = purport_paras_list

    else:
        purport_entry = None



    knowledge = {"page_info": navigation, "verse": verse_entry, "synonyms": synonyms, "translation": translation, "purport": purport_entry}
    
    json_knowledge = json.dumps(knowledge, indent=4, ensure_ascii=False)

    print(json_knowledge)
    print(type(json_knowledge))


    # Handling Directory creation.
    directory = Path(f'/home/somit/Projects/web-scraping/SB/1/{chapter}/')

    if not directory.exists():
        directory.mkdir()
    


    if Path(f'/home/somit/Projects/web-scraping/SB/1/{chapter}/{_index}.json').is_file():
        with open(f'/home/somit/Projects/web-scraping/SB/1/{chapter}/{_index}.json', 'w') as json_file:
            print(json_knowledge, file=json_file)
    else:
        with open(f'/home/somit/Projects/web-scraping/SB/1/{chapter}/{_index}.json', 'x') as json_file:
            print(json_knowledge, file=json_file)




# Driver Code for parser
chap = 19
total = 40
for chapter in range(chap,chap+1):
    for _index in range(1,total+1):
        url = f'https://vanisource.org/wiki/SB_1.{chapter}.{_index}'
        _source = requests.get(url)
        soup = BeautifulSoup(_source.content, 'html.parser')
        page_check = str(soup.find("div", {"class":"noarticletext mw-content-ltr"}))

        if page_check and str(page_check)!=str(None):
            continue
        else:
            print(_index)
            parser()

    # for _index in range(22,23):
    #     print(_index)
    #     parser()
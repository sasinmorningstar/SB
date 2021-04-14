import re

def current_id_replacements(current_id):
    current_id = current_id.replace('<h1 class="title" id="firstHeading">', '')
    current_id = current_id.replace('</h1>', '')
    return current_id


def verse_replacements(verse):
    verse = verse.replace('<div class="verse">', '')
    verse = verse.replace('</div>', '')
    verse = verse.replace('<dl>', '---')
    verse = verse.replace('</dl>', '')
    verse = verse.replace('<dd>', '')
    verse = verse.replace('</dd>', '')
    return verse


def synonyms_replacements(synonyms):
    synonyms = synonyms.replace('<div class="synonyms">', '')
    synonyms = synonyms.replace('<p>', '')
    synonyms = synonyms.replace('<i>', '')
    synonyms = synonyms.replace('</i>', '')
    synonyms = synonyms.replace('</p>', '')
    synonyms = synonyms.replace('</div>', '')
    return synonyms


def translation_replacements(translation):
    translation = translation.replace('<div class="translation">', '')
    translation = translation.replace('<p>', '')
    translation = translation.replace('</p>', '')
    translation = translation.replace('</div>', '')
    return translation


def purport_para_replacements(purport_para):
    purport_para = purport_para.replace('<p>', '')
    purport_para = purport_para.replace('</p>', '')
    purport_para = purport_para.replace('<b>', '')
    purport_para = purport_para.replace('</b>', '')

    purport_para = purport_para.replace('[', '')
    purport_para = purport_para.replace(']', '')
    purport_para = purport_para.replace(', ', '')

    purport_para = re.sub('(\(<a.*/a>\))','',purport_para)
    purport_para = re.sub('(<a.*/a>)','',purport_para)

    return purport_para


def purport_verse_replacements(purport_verse):
    purport_verse = purport_verse.replace('<dl>', '')
    purport_verse = purport_verse.replace('</dl>', '---')
    purport_verse = purport_verse.replace('<dd>', '')
    purport_verse = purport_verse.replace('</dd>', '')

    purport_verse = re.sub('(\(<a.*/a>\))','',purport_verse)
    purport_verse = re.sub('(<a.*/a>)','',purport_verse)

    return purport_verse
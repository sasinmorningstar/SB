import os
import json
import AdvancedHTMLParser

class Parser:
    def __init__(self, link):
        self.link = link
        self.htmlPath = self.getHtmlPath()
        self.jsonPath = self.getJSONPath()
        self.textId = self.getTextId()
        self.text = Text(self.textId)
        self.htmlParser = AdvancedHTMLParser.AdvancedHTMLParser()

        if not os.path.exists(self.htmlPath):
            # download html file from link, if not already present
            # downalod and save the html file to appropriate path  
            print("dummy")

        # parse the html file     
        self.htmlParser.parseFile(self.htmlPath)

    def getHtmlPath(self):
        # link -> htmlpath
        # Examples -
        # SB: https://vanisource.org/wiki/SB_2.1_Invocation --> ./books/html/sb/2/1/Invocation.html
        # BG: https://vanisource.org/wiki/BG_1.1_(1972) --> ./books/html/bg/1/1.html
        # CC: https://vanisource.org/wiki/CC_Adi_1.1_(1975) --> ./books/html/cc/adi/1/1.html
        return "./books/html/sb/1/1/1.html"

    # similarly JSONpath
    def getJSONPath(self):
        # eg: ./books/json/sb/2/1/Invocation.json
        return "./books/json/sb/1/1/1.json"
    
    def getTextId(self):
        # eg: https://vanisource.org/wiki/SB_2.1_Invocation --> sb/2/1/Invocation
        return "sb/1/1/1"

    def parseVerse(self):
        verses = self.htmlParser.getElementsByClassName("verse")

        # inform about unknown case of html not having even a single verse or more than one verse class
        if len(verses)!=1:
            print("non-single verse class", len(verses), self.link)

        for verse in verses[0].children:
            self.text.verses.append({
                "roman": verse.textContent
            })

    def save(self):
        open(self.jsonPath, "w").write(json.dumps(self.text.__dict__))
        print("saved")

        
class Text:
    def __init__(self, textId):
        self.info = {
            "id":textId,
        }
        self.verses = []
        self.synonyms = ""
        self.purport = []


p = Parser("https://vanisource.org/wiki/SB_1.1.1")
p.parseVerse()
p.save()




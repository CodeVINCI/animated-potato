import bs4
from bs4 import BeautifulSoup as soup

class UN:
    def news(self):
        file=open('/home/vinci/Desktop/So/Newsfiles/SyriaNews.html','r')
        page_html=file.read()
        pagesoup=soup(page_html,"html.parser")
        Headline=pagesoup.findAll("h4",{"id":"story-headline"})
        Headline=Headline[0]
        Headline=Headline.text

        img=pagesoup.findAll("a",{"id":"PhotoCrop"})
        img=img[0]
        img=img["href"]
        img=img[1:]
        img="/static/htmldownloads"+img


        Story=pagesoup.findAll("div",{"id":"fullstory"})
        Story=Story[0]
        Story=Story.findAll("p")
        Story=Story[1:]
        text=""
        for paragraphs in Story:
            text = text+paragraphs.text

        News=[img,Headline,text]
        return News

from bs4 import BeautifulSoup
from bs4 import NavigableString

from cdep_scraping.PLXBasicData import PLXBasicData

def cleanTitleText(titleText):
    titleText = titleText.replace('\n', '')
    return titleText

def plxMainTextToBasicData(htmlText:str)->PLXBasicData:
    # div class detalii-initiativa
    soup = BeautifulSoup(htmlText, 'html.parser')
    mainDiv = soup.find("div",{"class":"detalii-initiativa"})
    titleTag = mainDiv.find("h4")
    titleText = titleTag.text
    cleanedTitleText = cleanTitleText(titleText)
    dummyData = PLXBasicData()
    dummyData.BillName = cleanedTitleText
    return dummyData # WARNING: NOT FULLY IMPLEMENTED
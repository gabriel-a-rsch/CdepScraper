from typing import Any

from bs4 import BeautifulSoup
from bs4 import NavigableString

from cdep_scraping.PLXBasicData import PLXBasicData

def cleanTitleText(titleText):
    titleText = titleText.replace('\n', '')
    return titleText

def parseTable(table)->list[Any]:
    data = []
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    return data
def plxMainTextToBasicData(htmlText:str)->PLXBasicData:
    # div class detalii-initiativa
    soup = BeautifulSoup(htmlText, 'html.parser')
    mainDiv = soup.find("div",{"class":"detalii-initiativa"})
    titleTag = mainDiv.find("h4")
    titleText = titleTag.text
    cleanedTitleText = cleanTitleText(titleText)
    mainTable = mainDiv.find("table")
    data = parseTable(mainTable)
    print(data)
    dummyData:PLXBasicData = PLXBasicData()
    dummyData.BillName = cleanedTitleText
    dictionaryOfTableValues = {lst[0]: lst[1:] for lst in data}
    dummyData.PLXNumber = dictionaryOfTableValues['- Camera Deputaţilor:'][0]
    dummyData.BPINumber = dictionaryOfTableValues['- B.P.I.:'][0]
    dummyData.SenateNumber = dictionaryOfTableValues['- Senat:'][0]
    dummyData.Initiator = dictionaryOfTableValues['Initiator:'][0]
    dummyData.CurrentStage = dictionaryOfTableValues['Stadiu:'][0]
    dummyData.IsUrgentProcedure = dictionaryOfTableValues['Procedura de urgenta:'][0]
    dummyData.DecisionalChamber = dictionaryOfTableValues['Camera decizionala:'][0]
    dummyData.LegislativeProcedure =dictionaryOfTableValues['Procedura legislativa:'][0]
    dummyData.Character = dictionaryOfTableValues['Caracter:'][0]
    dummyData.GovNumber = dictionaryOfTableValues['- Guvern:'][0]
    dummyData.InitiativeType = cleanTitleText(dictionaryOfTableValues['Tip initiativa:'][0])
    return dummyData
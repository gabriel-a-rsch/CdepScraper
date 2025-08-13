from typing import Any

from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

from cdep_scraping.LegislativeProcedureStageInstance import LegislativeProcedureStageInstance
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

def parseLegislativeHistoryTableList(rawTableList:list[Any])->list[LegislativeProcedureStageInstance]:
    pass1 = [b for b in rawTableList if b] #remove empty entries
    pass2 = []
    currentMultiLenArray = pass1[0]
    pass2.append(currentMultiLenArray)
    for i in range(len(pass1)):
        if pass1[i][0] in currentMultiLenArray:
            continue
        else:
            currentMultiLenArray=pass1[i]
            pass2.append(currentMultiLenArray)
    #after pass 2 all duplicate entries are removed
    currentlyRelevantDate:str = ""
    currentIdentifier:str = ""
    pattern = re.compile(r"\d{2}(\.|-)\d{2}(\.|-)\d{4}")
    pass3:list[LegislativeProcedureStageInstance] = []
    for i in range(len(pass2)):
        firstStr = pass2[i][0]
        if len(firstStr)==2:
            currentIdentifier=firstStr
            continue
        if pattern.match(firstStr):
            currentlyRelevantDate=firstStr
        eventToDocumentStr = "\n".join(pass2[i][1:])
        auxLegInstance:LegislativeProcedureStageInstance = LegislativeProcedureStageInstance(currentlyRelevantDate,eventToDocumentStr,currentIdentifier) # ISSUE: this doesn't capture attachments
        pass3.append(auxLegInstance)
    pass3.pop(0)
    finalList = pass3
    return finalList


def plxMainTextToLegislativeProcedureList(htmlText:str)->list[LegislativeProcedureStageInstance]:
    soup = BeautifulSoup(htmlText,"html.parser")
    mainDiv=soup.find("div",{"id":"content"})
    mainTable=mainDiv.find("table",{"width":"100%", "border":"0", "cellspacing":"0", "cellpadding":"0"})
    myList = parseTable(mainTable)
    finalList = parseLegislativeHistoryTableList(myList)
    return finalList


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
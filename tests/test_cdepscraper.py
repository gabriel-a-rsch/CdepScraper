from cdep_scraping.LegislativeProcedureStageInstance import LegislativeProcedureStageInstance
from cdep_scraping.cdepParsing import plxMainTextToLegislativeProcedureList
from context import cdep_scraping
def test_cdepscraperPLXBasicData():
    file_path:str = 'samplePLXDetails.htm'
    magicTestName:str = """Proiect de Lege privind aprobarea Ordonanţei de urgenţă a Guvernului nr.132/2024 pentru modificarea şi completarea Legii nr.227/2015 privind Codul fiscal şi pentru completarea Legii nr.207/2015 privind Codul de procedură fiscală, precum şi pentru modificarea şi completarea unor acte normative"""
    magicBPINumber:str = "776/18-12-2024"
    magicPLXNumber:str = "9/03.02.2025"
    magicSenateNumber:str = "L607/2024"
    magicGovNumber:str = "E237/21.11.2024"
    magicLegislativeProcedure:str = "cf. Constitutiei revizuita în 2003"
    magicDecisionalChamber:str = "Camera Deputaţilor"
    magicInitiativeType:str = "Proiect de Lege pentru aprobarea O.U.G. nr. 132/2024"
    magicCharacter:str = "ordinar"
    magicUrgentProcedure:str = "da"
    magicCurrentStage:str = "trimis pentru raport la comisiile permanente ale Camerei Deputatilor"
    magicInitiator:str = "Guvern"
    with open(file_path, 'r', encoding="ISO-8859-2") as file:
        file_content = file.read()
    plxBasicData:cdep_scraping.PLXBasicData = cdep_scraping.cdepParsing.plxMainTextToBasicData(file_content)
    assert plxBasicData is not None
    assert plxBasicData.BillName is not None
    assert plxBasicData.BillName == magicTestName
    assert plxBasicData.BPINumber == magicBPINumber
    assert plxBasicData.PLXNumber == magicPLXNumber
    assert plxBasicData.SenateNumber == magicSenateNumber
    assert plxBasicData.GovNumber == magicGovNumber
    assert plxBasicData.LegislativeProcedure == magicLegislativeProcedure
    assert plxBasicData.DecisionalChamber == magicDecisionalChamber
    assert plxBasicData.InitiativeType == magicInitiativeType
    assert plxBasicData.Character == magicCharacter
    assert plxBasicData.IsUrgentProcedure == magicUrgentProcedure
    assert plxBasicData.CurrentStage == magicCurrentStage
    assert plxBasicData.Initiator == magicInitiator

def test_cdepscraperLegislativeHistory():
    file_path: str = 'samplePLXTable.htm'
    with open(file_path, 'r', encoding="ISO-8859-2") as file:
        file_content = file.read()
    testList:list[LegislativeProcedureStageInstance]= plxMainTextToLegislativeProcedureList(file_content)
    assert len(testList) == 7
    assert testList[0].identifier=="SE"
    assert testList[1].identifier=="CD"
    assert testList[0].date == "16.12.2024"
    assert testList[1].date == "03.02.2025"
    assert "prezentare în Biroul Permanent al Camerei Deputatilor" in testList[1].content
    assert "proiectul de lege" in testList[0].content


test_cdepscraperLegislativeHistory()
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

test_cdepscraperPLXBasicData()
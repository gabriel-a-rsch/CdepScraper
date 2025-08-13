from context import cdep_scraping
def test_cdepscraperPLXBasicData():
    file_path = 'PL-x nr. 9_2025.htm'
    testName = """Proiect de Lege privind aprobarea Ordonanţei de urgenţă a Guvernului nr.132/2024 pentru modificarea şi completarea Legii nr.227/2015 privind Codul fiscal şi pentru completarea Legii nr.207/2015 privind Codul de procedură fiscală, precum şi pentru modificarea şi completarea unor acte normative"""
    with open(file_path, 'r', encoding="ISO-8859-2") as file:
        file_content = file.read()
    plxBasicData:cdep_scraping.PLXBasicData = cdep_scraping.cdepParsing.plxMainTextToBasicData(file_content)
    assert plxBasicData is not None
    assert plxBasicData.BillName is not None
    assert plxBasicData.BillName == testName
test_cdepscraperPLXBasicData()
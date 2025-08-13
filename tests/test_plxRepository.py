from cdep_scraping.PLXRepository import PLXRepository
from context import cdep_scraping
def test_all():
    test_repo_export_to_JSONStr()
    test_repo_add_from_HTMLStr()

def test_repo_add_from_HTMLStr():
    repo:PLXRepository = PLXRepository()
    file_path:str="samplePLXDetails.htm"
    magicPLXNumber:str="9/03.02.2025"
    with open(file_path, 'r', encoding="ISO-8859-2") as file:
        file_content = file.read()
    repo.addPLXFromHTMLString(file_content)
    assert len(repo.plxList) == 1
    assert repo.plxList[0].basicData.PLXNumber == magicPLXNumber

def test_repo_export_to_JSONStr():
    repo:PLXRepository = PLXRepository()
    file_path:str="samplePLXDetails.htm"
    magicPLXNumber:str="9/03.02.2025"
    with open(file_path, 'r', encoding="ISO-8859-2") as file:
        file_content = file.read()
    repo.addPLXFromHTMLString(file_content)
    print(repo.exportToJSONStr())

# test_all()
test_repo_export_to_JSONStr()
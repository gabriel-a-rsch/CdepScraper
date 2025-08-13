import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from requests import Response

from cdep_scraping.PLXBasicData import PLXBasicData
from cdep_scraping.cdepParsing import plxMainTextToBasicData

class CDEPScraper:
    def __init__(self, cacheFolder:str=".webcache"):
        self.cacheFolder = cacheFolder;
        self.requestsSession = requests.Session()
        self.cachedSession = CacheControl(self.requestsSession, cache=FileCache(self.cacheFolder))
    def getPLXBasicDataFromURL(self, url:str)->PLXBasicData:
        response:Response = self.cachedSession.get(url)
        responseText = response.text
        return plxMainTextToBasicData(responseText)
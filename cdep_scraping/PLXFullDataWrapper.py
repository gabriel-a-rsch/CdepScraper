from cdep_scraping.LegislativeProcedureStageInstance import LegislativeProcedureStageInstance
from cdep_scraping.PLXAttachments import PLXAttachment
from cdep_scraping.PLXBasicData import PLXBasicData


class PLXFullDataWrapper:
    def __init__(self, basicData:PLXBasicData, Consultations:list[PLXAttachment], proceduralStages:list[LegislativeProcedureStageInstance]):
        self.basicData = basicData
        self.Consultations = Consultations
        self.ProceduralStages = proceduralStages
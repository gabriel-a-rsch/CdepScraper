from cdep_scraping.PLXAttachments import PLXAttachment


class LegislativeProcedureStageInstance:
    def __init__(self, date:str, content:str, attachments:list[PLXAttachment]=None):
        self.date = date
        self.content = content
        self.attachments = attachments
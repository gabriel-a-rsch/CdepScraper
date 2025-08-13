class PLXBasicData:
    def __init__(self):
        self.BillName = "" # mandatory
        self.PLXNumber = "" # mandatory
        self.BPINumber = "" #optional?
        self.SenateNumber = "" #optional
        self.GovNumber = "" #optional
        self.LegislativeProcedure="" # this is a formal string that should always have one of two values
        self.InitiativeType = ""
        self.Character = "" # regular value is "ordinar"
        self.CurrentStage = "" # many types of values here
        self.Initiator = "" # "Guvern" is a common type here
        self.DecisionalChamber = "" # Camera Decizionala
        self.IsUrgentProcedure = "" #




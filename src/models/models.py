from pydantic import BaseModel

class CreateInvestigation(BaseModel):
    type: str
    data: dict


class InvestigateRequest(BaseModel):
    file_path: str
    enrichment: dict
    

class Investigation(BaseModel):
    file_path: str

class SaveInvestigation(BaseModel):
    investigation_id: str
    name_of_investigation: str
    data: dict
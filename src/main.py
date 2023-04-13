from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import meilisearch
import utils
import consts
from models.models import Investigation, InvestigateRequest, CreateInvestigation


# Initialize the Meiisearch client
client = meilisearch.Client('http://localhost:7700')
client.create_index('investigations', {'primaryKey': 'id'})


# Initialize FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "The investigation service is runnning."}


# This makes the stix file to store our all SDOs, SCOs, and SROs. 
# This is file is to be used by the STIX Environment layer 
@app.post("/create_investigation")
async def create_investigation(data: CreateInvestigation):    
    try:
        investigation_data = utils.create_investigation(data)
        if investigation_data is not None:
            return investigation_data
        else:
            raise HTTPException(400, detail="could not create investigation")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

"""
This will take the ioc and the list of analyzers to run
"""
@app.post("/investigate")
async def investigate(investigate_request: InvestigateRequest):
    investigated, error = utils.preform_investigation(investigate_request)
    if investigated:
        return Response(status_code=204)
    else:
        raise HTTPException(500, detail=str(error))

@app.post("/display")
async def display_investigation(investigation: Investigation):
    try:
        data = utils.display_investigation(investigation)
        return Response(status_code=200, content=data)
    except Exception as e:
        raise HTTPException(500, detail=str(e))



@app.get("/get_investigation_types")
async def get_all_stix_types():
    try:
        stix_types = consts.investigation_types
        return stix_types
    except Exception as e:
        raise HTTPException(500, detail=str(e))
import database as db
from sqlalchemy import *
from sqlalchemy.orm import *

from fastapi import FastAPI

crud = FastAPI()

@crud.get("/get_api_key_info")
def getAPIKey(apiID : str):
    with db.s : 
        getStmt = select(db.APIKeys).where(db.APIKeys.id == apiID)
        return db.s.scalars(getStmt).all()


@crud.get("/get_available_api_key")
def getAvailableAPIKey():
    with db.s : 
        getStmt = select(db.APIKeys.id).where(db.APIKeys.isAvailable == True)
        return db.s.scalars(getStmt).all()

@crud.get("/add_api_key") 
def addAPIKey(apiID : str, apiName = ''):
    apiToAdd = db.APIKeys(id = apiID, name=apiName, isAvailable = True)    
    db.s.add(apiToAdd)
    db.s.commit()
    db.s.refresh(apiToAdd)
    return apiToAdd

@crud.get("/delete_api_key_id")
def deleteAPIKeyByID(apiID : str) :
    deleteStm = (
        delete(db.APIKeys)
        .where(db.APIKeys.id == apiID)
)
    db.s.execute(deleteStm)
    db.s.commit()

@crud.get("/delete_api_key_name")    
def deleteAPIKeyByName(apiName : str) :
    if apiName == '':
        raise Exception("INVALID NAME : please provide a valid name")
    deleteStm = (
        delete(db.APIKeys)
        .where(db.APIKeys.name == apiName)
)
    db.s.execute(deleteStm)
    db.s.commit()


@crud.get("/api_availability")
def setAPIAvailability(apiID : str, availability : bool):
    updateStm = update(db.APIKeys).values(isAvailable = availability).where(db.APIKeys.id == apiID)
    db.s.execute(updateStm)
    print("Updated the availability")
    db.s.commit()

@crud.get("/set_name")
def setName(apiID : str, apiName : str):
    if len(getAPIKey(apiID)) == 1 :
        updateStm = update(db.APIKeys).values(name = apiName).where(db.APIKeys.id == apiID)
        db.s.execute(updateStm)
        print("Updated the name")
        db.s.commit()       
        return getAPIKey(apiID)
    raise Exception("No Such API key")    
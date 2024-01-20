import database as db
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.orm import *

from fastapi import FastAPI



# def after_delete_listener(s, instance):
#     print(f"{instance} was deleted")

# event.listen(db.s, "after_delete", after_delete_listener)

crud = FastAPI()

@crud.get("/get_api_key_info", tags=["Get API Key"])
def getAPIKey(apiID : str):
    with db.s : 
        getStmt = select(db.APIKeys).where(db.APIKeys.id == apiID)
        return db.s.scalars(getStmt).all()


@crud.get("/get_available_api_key", tags=["Get API Key"])
def getAvailableAPIKey():
    with db.s : 
        getStmt = select(db.APIKeys.id).where(db.APIKeys.isAvailable == True)
        return db.s.scalars(getStmt).all()

@crud.get("/add_api_key", tags=["Add API key"]) 
def addAPIKey(apiID : str, apiName = ''):
    apiToAdd = db.APIKeys(id = apiID, name=apiName, isAvailable = True)    
    db.s.add(apiToAdd)
    db.s.commit()
    db.s.refresh(apiToAdd)
    successMessage = {
        "status" : "success",
        "message" : "API ADDED SUCCESSFULLY "  ,
        "data" : getAPIKey(apiID)
        } 
    return successMessage

@crud.get("/delete_api_key_id", tags=["Delete API key"])
def deleteAPIKeyByID(apiID : str) :
    if len(getAPIKey(apiID)) == 0:
        return "NO SUCH API"
    deleteStm = (
        delete(db.APIKeys)
        .where(db.APIKeys.id == apiID)
)
    db.s.execute(deleteStm)
    db.s.commit()
    successMessage = {
        "status" : "success",
        "message" : "DELETED : " + apiID,
        "data" : null
        } 
    return successMessage

@crud.get("/delete_api_key_name", tags=["Delete API key"])    
def deleteAPIKeyByName(apiName : str) :
    if apiName == '':
        raise Exception("INVALID NAME : please provide a valid name")
    deleteStm = (
        delete(db.APIKeys)
        .where(db.APIKeys.name == apiName)
)
    db.s.execute(deleteStm)
    db.s.commit()
    successMessage = {
        "status" : "success",
        "message" : "DELETED : " + apiName,
        "data" : null
        } 
    return successMessage

@crud.get("/api_availability", tags=["Change API Key Attribute"])
def setAPIAvailability(apiID : str, availability : bool):
    updateStm = update(db.APIKeys).values(isAvailable = availability).where(db.APIKeys.id == apiID)
    db.s.execute(updateStm)
    print("Updated the availability : " + apiID)
    db.s.commit()
    successMessage = {
        "status" : "success",
        "message" : "Updated the availability successfully",
        "data" : getAPIKey(apiID)
    }
    return successMessage

@crud.get("/set_name", tags=["Change API Key Attribute"])
def setName(apiID : str, apiName : str):
    if len(getAPIKey(apiID)) == 1 :
        updateStm = update(db.APIKeys).values(name = apiName).where(db.APIKeys.id == apiID)
        db.s.execute(updateStm)
        print("Updated the name")
        db.s.commit()   
        successMessage = {
            "status" : "success",
            "message" : "UPDATED NAME TO: " + getAPIKey(apiID)[0].name,
            "data" : getAPIKey(apiID)
        }    
        return successMessage
    failedMessage = {
        "status" : "failed",
        "message" : "No Such API key",
        "data" : null
    }
    raise Exception(failedMessage)    
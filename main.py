from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

import modes.mode as generalMode
import modes.gptMode as gpt

  
import starlette.status as status
import schemas
import requests

from typing_extensions import Annotated

import axios

chibi_nlp = FastAPI()




def modeMaker(inpMode : str) :
    if inpMode == 'gpt' :
        res = gpt.GptMode
        # sum(res)


        return res
    if inpMode == 'artin' :
        pass
    print("invalid mode")
    return -1    



@chibi_nlp.get("/")
def decideModeAndAction():
    # inpAction = input("Enter requiered action")


    inpMode = input("Enter mode : ")
    mode = modeMaker(inpMode)

    inpAction = input("Enter Action : ")
    #TODO send a request to summerize
    print("Sending request...")
    if inpAction == 'summerize':
        url = f"http://127.0.0.1:8000/summerize/?inpMode={inpMode}"
    elif inpAction == 'paraphrase':
        url = f"http://127.0.0.1:8000/paraphrase/?inpMode={inpMode}"         
    
    response = requests.get(url,mode)

    print(f"Response : \n", response)




@chibi_nlp.get("/summerize/")
def sum(inpMode :  str, my_dependency: dict = Depends(modeMaker)):
    mode = modeMaker(inpMode)
    text = "Konnichiwa!Summerize!"
    res = print(mode.summerize(mode, text))
    return res




@chibi_nlp.get("/paraphrase/")
def paraphrase(inpMode :  str, my_dependency: dict = Depends(modeMaker)):
    mode = modeMaker(inpMode)
    text = "Konbanwa!Para-chan!"
    res = mode.paraphrase(mode, text)
    print(res)
    return res



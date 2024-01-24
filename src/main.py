from fastapi import FastAPI, Query

import schemas
import os, sys


from typing import Literal
import modes.gptMode as gpt

modeList = ['gpt', 'artin']

port = 8000
chibi_nlp = FastAPI()


paraphrasePreText = 'please paraphrase the following paragraph in its native language and return it in a json format with ParaphrasedText as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences'
summerizePreText = 'please summerize the following paragraph in its native language and return it in a json format with summerizedText as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences'

actions = ['summerize', 'paraphrase']

def modeMaker(inpMode : str) :
    if inpMode == 'gpt' :
        res = gpt.GptMode


        res.client = gpt.createOpenAiConnection()
        return res
    if inpMode == 'artin' :
        pass

    # raise Exception("Invalid Mode")





modes = {}
for m in modeList :
    mode = modeMaker(m)
    modes[m] = mode

methods = {}
@chibi_nlp.get("/")
def getModeList(action : str = Query(enum= actions)):
    resModes = []
    for mKey in list(modes.keys()) :
        m = modes.get(mKey)
        methodList = [func for func in dir(m) if callable(getattr(m, func)) and not func.startswith("__")]
        methods[mKey] = methodList
        if action in methodList :
            modeName = mKey
            resModes.append(modeName)
    #TODO : add a stanard format for answer
    return(resModes)        




def modeActionValidator(modeAction : schemas.ModeAction):
    if modeAction.mode not in modes.keys():
        raise Exception(f"There is no mode with name : {modeAction.mode}")
    if modeAction.mode not in getModeList(modeAction.action):
        raise Exception(f"The Mode {modeAction.mode} doesn't have a summerize method")



@chibi_nlp.get("/summerize/")
def sum(input : schemas.SummerizeInput):
    modeAction = schemas.ModeAction(mode=input.inpMode, action='summerize')
    modeActionValidator(modeAction)
    mode = modes[input.inpMode]
    res = mode.summerize(mode, input.text, input.preText)
    print(res)
    return res
    
# TODO : uncomment the true paraModeList after test
# paraModeList = [i for i in getModeList('paraphrase')]
paraModeList = ['gpt','artin']

@chibi_nlp.get("/paraphrase/")
def paraphrase( text : str, inpMode :  str = Query(enum=paraModeList) , preText : str = paraphrasePreText, numberOfRequest : int = Query(lt=50, gt=0)):
    modeAction = schemas.ModeAction(mode=inpMode, action='paraphrase')
    modeActionValidator(modeAction)
    mode = modes[inpMode]
    print(f"preText = {preText}")
    res = mode.paraphrase(mode, text, numberOfRequest,preText)
    print(res)
    return res



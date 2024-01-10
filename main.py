from fastapi import FastAPI

import modes.gptMode as gpt
import schemas



modeList = ['gpt', 'artin']


port = 8000
chibi_nlp = FastAPI()


paraphrasePreText = 'please paraphrase the following paragraph in its native language and return it in a json format with \"ParaphrasedText\" as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences\n'
summerizePreText = 'please summerize the following paragraph in its native language and return it in a json format with \"summerizedText\" as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences\n'

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
def getModeList(action : str):
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


    #     url = f"http://127.0.0.1:8000/summerize/?inpMode={inpMode}&text={inpText}"

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
    




@chibi_nlp.get("/paraphrase/")
def paraphrase(inpMode :  str, text : str, preText : str = paraphrasePreText):
    # modeActionValidator(inpMode, 'paraphrase')
    mode = modes[inpMode]
    print(f"preText = {preText}")
    res = mode.paraphrase(mode, text, preText)
    print(res)
    return res




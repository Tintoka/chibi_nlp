from pydantic import BaseModel
import modes.mode as generalMode

paraphrasePreText = 'please paraphrase the following paragraph in its native language and return it in a json format with \"ParaphrasedText\" as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences\n'
summerizePreText = 'please summerize the following paragraph in its native language and return it in a json format with \"summerizedText\" as key? please dont type anything else and try to maintain writers structure,if the text has lot of slang use a lot of slang, if its formal use formal words and sentences\n'

class Mode(BaseModel):
    mode : type

class ModeAction(BaseModel):
    mode : str
    action : str


class ActionInput(BaseModel):
    inpMode :  str
    text : str
    preText: str 

class SummerizeInput(ActionInput):
    preText : str = summerizePreText

class ParahraseInput(ActionInput):
    preText : str = paraphrasePreText    
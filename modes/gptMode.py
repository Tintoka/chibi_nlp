from . import mode
import json
import time

from openai import OpenAI, RateLimitError

import backoff
import os
#from dotenv import load_dotenv
import crud 
#load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MAX_REQUEST_NUMBER = 200

port = 5000
i : int = -1


def timeStamp():
    curTime = time.time()
    return time.ctime(curTime)


def createOpenAiConnection():
    #get a valid API_KEY from the database(or ask another API)
    global i 
    i = ( i + 1 ) % len(crud.getAvailableAPIKey()) 
    apiKey = crud.getAvailableAPIKey()[abs(i)]

    #Create and return a conenction with that API_KEY
    client = OpenAI(api_key=apiKey)
    apiName = crud.getAPIKey(apiKey)[0].name
    print("***********************************")
    print(f"created gpt client from {apiName}!")
    print("***********************************")
    return client


class GptMode(mode.Mode):
    client = []
    def __init__(self):
        print(f"reqNum = {self.reqNum}")
        self.client = createOpenAiConnection()

    def preprocess(self, action, text, preText, numOfReq) -> str:
        if action == 'summerize':
            return (preText + text)
        
        if action == 'paraphrase':
            preText = preText.replace("[placeholder_numberOfRequest]", str(numOfReq))
            # numOfReqStr = str(numOfReq)
            # resText = 
            return (preText + text)

    def postprocess(self, text):
        resText = text.splitlines()
        resJson = {"paraphrased Texts" : resText}
        message = {
            "status" : "success",
            "message" : "paraphrased the text successfully",
            "version" : "3.5-turbo",
            "time" : timeStamp(),
            "data" :  resJson
        }
        print(f"Message : {message}")
        return (message)
    
    # @backoff.on_exception(backoff.expo, RateLimitError)
    def summerize(self, text : str, numOfReq : int , preText ) -> str:
        preprocessedText = self.preprocess(self,'summerize', text, preText, numOfReq)
        if  self.reqNum > MAX_REQUEST_NUMBER :
            self.client = createOpenAiConnection()
            print("Created a New Connection!")
            self.reqNum = 0
        print("Sending summerize request to GPT...")
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": preprocessedText},
                {"role": "user", "content": preprocessedText}
            ]
        )
        self.reqNum += 1
        print("Sent GPT REQUEST!")
        paraphrasedText = completion.choices[0].message.content



        summerizedText =  ("GPT summerized the text~ , " + preprocessedText)
        return self.postprocess(self, summerizedText) 
    
    # @backoff.on_exception(backoff.expo, RateLimitError)
    def paraphrase(self, text, preText, numOfReq : int):
        preprocessedText = self.preprocess(self, 'paraphrase', text, preText, numOfReq)
        self.client = createOpenAiConnection()
        print("Sending request to GPT...")
        try:
            completion = self.client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": preprocessedText},
                    {"role": "user", "content": preprocessedText}
                ]
            )
            # self.reqNum += 1
            print("Sent GPT REQUEST!")

            paraphrasedText = completion.choices[0].message.content
            # paraphrasedText = { "ParaphrasedText": preText + text}
            print(paraphrasedText)
            # paraphrasedText = "Paraphrased Text mutant~"
            # paraphrasedText = "GPT paraphrased this Text~, " + preprocessedText
            return self.postprocess(self, paraphrasedText)
        except RateLimitError as e:
            errorMessage = {
                "state" : "failed",
                "message" : f"OpenAI API : request exceeded rate limit: {e}",
                "data" : []
            }
            return(errorMessage) 


    

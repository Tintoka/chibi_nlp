from . import mode
import json

from openai import OpenAI, RateLimitError

import backoff
import os
from dotenv import load_dotenv
import crud 
load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MAX_REQUEST_NUMBER = 200

port = 5000


def createOpenAiConnection():
    #get a valid API_KEY from the database(or ask another API)
    apiKey = crud.getAvailableAPIKey()[0]
    # print("Fetched API Key : ", apiKey)
    
    #Create and return a conenction with that API_KEY
    client = OpenAI(api_key=apiKey)
    print("created gpt client!")
    return client


class GptMode(mode.Mode):
    client = []
    def __init__(self):
        print(f"reqNum = {self.reqNum}")
        self.client = createOpenAiConnection()

    def preprocess(self, action, text, preText) -> str:
        if action == 'summerize':
            return (preText + text)
        
        if action == 'paraphrase':
            return (preText + text)

    def postprocess(self, text):
        return (f'++++++ {text}) +++++++')
    
    @backoff.on_exception(backoff.expo, RateLimitError)
    def summerize(self, text : str, preText) -> str:
        preprocessedText = self.preprocess(self,'summerize', text, preText)
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
        paraphrasedText = completion.choices[0].message



        summerizedText =  ("GPT summerized the text~ , " + preprocessedText)
        return self.postprocess(self, summerizedText) 
    
    @backoff.on_exception(backoff.expo, RateLimitError)
    def paraphrase(self, text, preText):
        preprocessedText = self.preprocess(self, 'paraphrase', text, preText)
        if  self.reqNum > MAX_REQUEST_NUMBER :
            self.client = createOpenAiConnection()
            print("Created a New Connection!")
            self.reqNum = 0
        print("Sending request to GPT...")
        completion = self.client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": preprocessedText},
                {"role": "user", "content": preprocessedText}
            ]
        )
        self.reqNum += 1
        print("Sent GPT REQUEST!")
        paraphrasedText = completion.choices[0].message
#         paraphrasedText = {
# "ParaphrasedText": preText + text}
#         print(paraphrasedText['ParaphrasedText'])

        # paraphrasedText = "GPT paraphrased this Text~, " + preprocessedText
        return self.postprocess(self, paraphrasedText)
    

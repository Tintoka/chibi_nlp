import json

class CustomEncoder(json.JSONEncoder):
    def default(
        self,
        o,
    ):

        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)





class Mode():

    def __call__(self):
        return self.__init__()

    def preprocess(self, action, text):
        pass

    def postprocess(self, text):
        pass

    def summerize(self, text : str) -> str:
        pass


class GptMode(Mode):



    def preprocess(self, action, text) -> str:
        if action == 'summerize':
            return (f"^o^/ {text} \^o^")
        
        if action == 'paraphrase':
            return (f'^-^~~ {text} ~~^-^')

    def postprocess(self, text):
        return (f'++++++ {text}) +++++++')

    def summerize(self, text : str) -> str:
        readyText = self.preprocess(self,'summerize', text)
        summerizedText =  ("GPT summerized the text~ , " + readyText )
        return self.postprocess(self, summerizedText) 

    def paraphrase(self, text):
        preprocessedText = self.preprocess(self, 'paraphrase', text)
        paraphrasedText = "GPT paraphrased this Text~, " + preprocessedText
        return self.postprocess(self, paraphrasedText)
    

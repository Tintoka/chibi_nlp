class Mode():
    reqNum : int = 0
    def preprocess(self, action, text):
        pass

    def postprocess(self, text):
        pass

    def summerize(self, text : str) -> str:
        pass

    def paraphrase(self, text : str) -> str:
        pass
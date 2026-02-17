import os

class Parser:
    def __init__(self, dataPath : str, outputFolder : str) -> None:
        self.dataPath = dataPath
        self.outputFolder = outputFolder
        os.makedirs(self.outputFolder, exist_ok = True)

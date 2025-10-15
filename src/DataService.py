from src.BestiaryParser import BestiaryParser

class DataService():
    def __init__(self, dataPath : str, outputFolder : str) -> None:
        self.dataPath : str = dataPath
        self.outputFolder : str = outputFolder

    def generateMonsterList(self) -> None:
        bp = BestiaryParser(self.dataPath, self.outputFolder)
        bp.generateMonsterList()
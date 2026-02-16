from src.BestiaryParser import BestiaryParser
from src.SpellParser import SpellParser
import os

class DataService():
    def __init__(self, mainDataPath : str, outputFolder : str) -> None:
        self.mainDataPath : str = mainDataPath
        self.outputFolder : str = outputFolder

        self.bestiaryParser = BestiaryParser(os.path.join(self.mainDataPath, 'bestiary'), os.path.join(self.outputFolder, 'bestiary'))
        self.spellParser = SpellParser(os.path.join(self.mainDataPath, 'spells'), os.path.join(self.outputFolder, 'spells'))


    def generateMonsterList(self) -> None:
        self.bestiaryParser.generateMonsterList()


    def generateSpellList(self) -> None:
        self.spellParser.generateSpellList()
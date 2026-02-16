import os
import json
import sys
sys.path.append('.')
import re
from tqdm import tqdm

class SpellParser:
    def __init__(self, dataPath : str, outputFolder : str) -> None:
        self.dataPath = dataPath
        self.outputFolder = outputFolder
        if not os.path.exists(self.outputFolder):
            os.mkdir(self.outputFolder)


    def generateSpellList(self)->None:
        pass
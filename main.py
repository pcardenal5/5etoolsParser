from src.DataService import DataService
import os

mainDataPath = './5etools-v2.13.0/data'
outputFolder = './5etools'
ds = DataService(os.path.join(mainDataPath, 'bestiary'), outputFolder = outputFolder)
ds.generateMonsterList()
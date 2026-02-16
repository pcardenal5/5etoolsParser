from src.DataService import DataService

mainDataPath = './5etools-v2.24.3/data'
outputFolder = './5etools'
ds = DataService(mainDataPath, outputFolder)
ds.generateMonsterList()
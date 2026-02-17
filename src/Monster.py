from typing import Any
from jinja2 import Environment, FileSystemLoader
from math import floor
import os

from src.ActionTrait import ActionTrait
from src.Models.MonsterModel import ImmunitiesModel, MonsterModel, VulnerabilitiesModel, ResistancesModel

class Monster:
    def __init__(self, data : dict[str, Any], source : str, outputFolder : str) -> None:
        self.environment = Environment(loader = FileSystemLoader('templates/'))
        self.template = self.environment.get_template('monster.md')

        self.model = MonsterModel.model_validate(data, extra = 'forbid')
        self.source = source
        self.name = self.model.name.replace('/','-').replace(':', '').replace('"','').title()
        self.size = self.model.size
        self.type = self.model.type
        self.cr = self.model.cr
        self.alignment = self.model.alignment
        self.ac = self.model.ac
        self.hp = self.model.hp
        self.str = self.model.str_
        self.dex = self.model.dex_
        self.con = self.model.con_
        self.int = self.model.int_
        self.wis = self.model.wis_
        self.cha = self.model.cha_

        self.strMod = self.calculateModifier(self.str)
        self.dexMod = self.calculateModifier(self.dex)
        self.conMod = self.calculateModifier(self.con)
        self.intMod = self.calculateModifier(self.int)
        self.wisMod = self.calculateModifier(self.wis)
        self.chaMod = self.calculateModifier(self.cha)

        self.saves = self.model.save

        self.strSave = self.getSave('str')
        self.dexSave = self.getSave('dex')
        self.conSave = self.getSave('con')
        self.intSave = self.getSave('int')
        self.wisSave = self.getSave('wis')
        self.chaSave = self.getSave('cha')

        self.speed = self.parseSpeed(self.model)
        self.skill = self.parseSkill(self.model)
        self.senses = self.parseSenses(self.model)
        self.languages = self.parseLanguages(self.model)

        self.legendaryGroup = self.model.legendaryGroup
        self.parseLegendaryGroup()

        self.resist = self.model.resist
        self.vulnerable = self.model.vulnerable
        self.immune = self.model.immune
        self.conditionImmune = self.model.conditionImmune
        self.buildResistances()


        self.outputFolder = outputFolder
        self.monsterOutputFolder = os.path.join(self.outputFolder, 'ByCR', str(self.cr).replace('/', '-').replace('l','1').replace('00','0'))
        self.completeOutputPath = os.path.join(self.monsterOutputFolder, self.name) + '.md'
        if not os.path.exists(self.monsterOutputFolder):
            os.makedirs(self.monsterOutputFolder)

        self.traits = self.parseActionTraits('trait')
        self.actions = self.parseActionTraits('action')
        self.bonus = self.parseActionTraits('bonus')
        self.legendary = self.parseActionTraits('legendary')

        self.buildActionTraits()


    def parseActionTraits(self, actionTraitType : str) -> str:
        actionTrait = self.model.__getattribute__(actionTraitType)
        if actionTrait is None:
            return ''
        traitType = type(actionTrait) # pyright: ignore
        if traitType not in (list, dict):
            raise NotImplementedError('Type not supported')

        if traitType == list:
            return '\n'.join([ActionTrait(trait, self.name, self.environment, actionTraitType, self.outputFolder).completeText for trait in actionTrait]) # type: ignore

        return '\n'.join([ActionTrait(actionTrait, self.name, self.environment, actionTraitType, self.outputFolder).completeText])# type: ignore


    def buildResistances(self) -> None:
        self.resistances = ''

        if self.resist is not None:
            self.resistances += '**Resistances**: ' + self.parseDamagemodifiers(self.resist) + '\n\n'
        if self.vulnerable is not None:
            self.resistances += '**Vulnerabilities**: ' + self.parseDamagemodifiers(self.vulnerable) + '\n\n'
        if self.immune is not None:
            self.resistances += '**Damage Immunities**: ' + self.parseDamagemodifiers(self.immune) + '\n\n'
        if self.conditionImmune is not None:
            self.resistances += '**Condition Immunities**: ' + self.parseDamagemodifiers(self.conditionImmune) + '\n\n'


    @staticmethod
    def parseDamagemodifiers(modifier : list[str] | list[str|ResistancesModel] | list[str|VulnerabilitiesModel] | list[str|ImmunitiesModel]) -> str:
        outputList : list[str] = []
        for item in modifier:
            outputList.append(item.__str__())
        return ', '.join(outputList)


    def buildActionTraits(self) -> None:
        self.actionTraits = ''
        if self.traits != '':
            self.actionTraits += f'## Traits\n\n{self.traits}\n\n'
        if self.actions != '':
            self.actionTraits += f'## Actions\n\n{self.actions}\n\n'
        if self.legendary != '':
            self.actionTraits += f'## Legendary Actions\n\n{self.legendary}\n\n'


    def generateText(self) -> str:
        return self.template.render(self.__dict__)

    @staticmethod
    def calculateModifier(stat: int) -> int:
        return int(floor(stat/2.) - 5)


    def getSave(self, stat : str) -> int:
        baseValue = self.saves.get(stat.lower())
        if baseValue:
            return int(baseValue.replace('+', ''))

        return self.__getattribute__(stat + 'Mod')


    def parseLegendaryGroup(self) -> None:
        if self.legendaryGroup is None:
            return
        self.legendaryGroup = f'![[Legendary Group {self.legendaryGroup['name']}_{self.legendaryGroup['source']}|Legendary Group {self.legendaryGroup['name']}]]' #type: ignore
        return


    @staticmethod
    def parseSpeed(model : MonsterModel) -> str:
        if model.speed:
            return f'**Speed**: {model.speed}\n'
        return ''


    @staticmethod
    def parseSkill(model : MonsterModel) -> str:
        if model.skill:
            return f'**Skills**: {model.skill}\n'
        return ''



    @staticmethod
    def parseSenses(model : MonsterModel) -> str:
        if model.senses:
            return f'**Senses**: {model.senses}\n'
        return ''



    @staticmethod
    def parseLanguages(model : MonsterModel) -> str:
        if model.languages:
            return f'**Languages**: {model.languages}\n'
        return ''


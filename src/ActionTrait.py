from jinja2 import Environment
import re

class ActionTrait():
    def __init__(self, actionTrait : dict, monsterName: str, environment : Environment, actionTraitType: str, outputFolder : str) -> None:
        # Jinja setup
        self.environment = environment
        self.template = self.environment.get_template('ActionTrait.md')

        self.data = actionTrait


        self.actionTraitType = actionTraitType
        self.monsterName = monsterName
        self.name = self.data.get('name', 'None')
        self.name = re.sub(r'\[\[rest.+?#.+?\|(.+?)\]\]', r'\1', self.name)
        self.name = re.sub(r'\[\[(.+?)\]\]', r'\1', self.name)

        self.mainOutputFolder = outputFolder

        if self.data.get('text'):
            self.text = self.data['text']
        elif self.data.get('entries') is not None:
            self.text = self.parseActionEntries(self.data['entries'])
        else:
            self.text = ''



        self.attack = self.data.get('attack', '')
        self.parseText()
        self.parseAttack()

        self.completeText = self.generateText()


    def parseText(self) -> None:
        if type(self.text) == list:
            self.text = '\n'.join([t for t in self.text if t is not None])
        self.text.replace('•', '- ')
        self.text = self.text.replace('ft.', 'ft')
        # Before replacint the monster's name by "the creature" we searhc for all existing links.
        # They are replaced by link0, link1, ..., linkN so as not to replace them with "the creature"
        #  and create false links. They are later replaced back
        linksInString = re.findall(r'(\[\[.+?\]\])',self.text)
        if not linksInString:
            return
        # Get unique elements
        used = set()
        unique = [x for x in linksInString if x not in used and (used.add(x) or True)]

        for i in range(len(unique)):
            self.text = self.text.replace(linksInString[i], f'link{i}')
        for i in range(len(linksInString)):
            self.text = self.text.replace(f'link{i}', linksInString[i])




    def parseActionEntries(self, actionTraitList: list) -> str:
        actionText = ''
        for item in actionTraitList:
            actionText += self.parseActionEntryElement(item) + '\n'
        return actionText


    def parseActionEntryElement(self, actionTrait) -> str:
        if isinstance(actionTrait, str):
            return actionTrait

        actionText = ''
        if isinstance(actionTrait, dict):
            if not actionTrait.get('items'):
                return ActionTrait(
                    actionTrait,
                    self.monsterName,
                    environment = self.environment,
                    actionTraitType = self.actionTraitType,
                    outputFolder = self.mainOutputFolder
                ).completeText


            for element in actionTrait['items']:
                if isinstance(element, dict):
                    if element.get('entry'):
                        key = 'entry'
                    else:
                        key = 'entries'
                    actionText += f'\n- **{element['name'].title()}** : {self.parseActionEntryElement(element[key])}\n'

                if isinstance(element, str):
                    actionText += f'\n{element}\n'

            return actionText

        if isinstance(actionTrait, list):
            return ''.join(actionTrait)

        raise TypeError(f'ActionEntryElement not supported({type(actionTrait)}): {actionTrait}')


    def parseAttack(self) -> None:
        if type(self.attack) == list:
            self.attack = '\n'.join([t for t in self.attack if t is not None])
        self.attack.replace('•', '- ')
        if self.attack != '':
            self.attack = f'\n{self.attack}\n'



    def generateText(self) -> str:
        if self.name.lower().__contains__('spellcasting'):
            return self.parseSpellcasting()
        return self.template.render(self.__dict__)



    def parseSpellcasting(self) -> str:
        if not self.data:
            return ''

        s = ''
        if isinstance(self.data, dict):
            s += f'### {self.data['name']}\n'
            if self.data.get('headerEntries'):
                s += f'{''.join(self.data['headerEntries'])}\n'
            if self.data.get('spells'):
                s += self.parseSpells(self.data['spells'])
            if self.data.get('will'):
                s += self.parseAtWillSpells(self.data['will'])
            if self.data.get('daily'):
                s += self.parseDailySpells(self.data['daily'])
        elif isinstance(self.data, str):
            pass
        else:
            raise TypeError(f'Type not considered for spellcasting item({type(self.data)}): {self.data}')

        return s


    @staticmethod
    def parseDailySpells(data: dict[str, list[str|dict[str,str]]]) -> str:
        ds = ''
        for key, value in data.items():
            ds += f'- {key.replace('e', ' per day each')}: '
            for item in value:
                if isinstance(item, str):
                    ds += f'{item}, '
                elif isinstance(item, dict):
                    if not item.get('hidden', False):
                        ds += f'{item['entry']}, '
                else:
                    raise TypeError(f'Type not considered for daily spell element({type(item)}) : {item}')
            ds = ds.strip().removesuffix(',')
            ds += '\n'
        return ds


    @staticmethod
    def parseAtWillSpells(data: list) -> str:
        ws = '- At will: '
        for value in data:
            if isinstance(value, str):
                ws += f'{value}, '
            elif isinstance(value, dict):
                if not value.get('hidden', False):
                    ws += f'{value['entry']}, '
            else:
                raise TypeError(f'Type not considered for at-will spell element({type(value)}) : {value}')
        ws += '\n'
        return ws


    @staticmethod
    def parseSpells(data : dict[str, dict]) -> str:
        s = ''
        for key, value in data.items():
            s += f'- {key}'
            if value.get('slots'):
                s += f' ({value['slots']} slots)'
            s += f': {', '.join(value['spells'])}.\n'
        return s


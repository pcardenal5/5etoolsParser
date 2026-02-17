from pydantic import BaseModel, Field
from typing import Optional, override

class HealthPointsModel(BaseModel):
    average : int
    formula : str


class ResistancesModel(BaseModel):
    resist : list[str]
    note : str
    cond : bool


    @override
    def __str__(self) -> str:
        return f"{','.join(self.resist)} {self.note}"


class ImmunitiesModel(BaseModel):
    immune : list[str]
    note : str
    cond : bool


    @override
    def __str__(self) -> str:
        return f"{','.join(self.immune)} {self.note}"

class VulnerabilitiesModel(BaseModel):
    vulnerable : list[str]
    note : str
    cond : bool

    @override
    def __str__(self) -> str:
        return f"{','.join(self.vulnerable)} {self.note}"


class TraitModel(BaseModel):
    name : str
    entries : list[str]


class ActionModel(BaseModel):
    name : str
    entries : list[str]


class SpellModel(BaseModel):
    slots : Optional[int] = None
    spells : list[str]


class SpellcastingModel(BaseModel):
    name : str
    type : str
    headerEntries: list[str]
    will : Optional[list[str]] = None
    daily : Optional[dict[str, list[str]]] = None
    spells : Optional[dict[str, SpellModel]] = None
    ability : str



class MonsterModel(BaseModel):
    name: str
    shortName : Optional[bool] = None
    isNamedCreature : Optional[bool] = None
    source: str
    page: int
    srd : Optional[bool] = None
    referenceSources : Optional[list[str]] = None
    reprintedAs : Optional[list[str]] = None
    size: list[str]
    type: str|dict[str,str|list[str]]
    alignment: list[str]
    alignmentPrefix: Optional[str] = None
    ac: list[dict[str, int|list[str]]]
    hp: HealthPointsModel

    speed: dict[str, int]
    str_: int = Field(alias = 'str')
    dex_: int = Field(alias = 'dex')
    con_: int = Field(alias = 'con')
    int_: int = Field(alias = 'int')
    wis_: int = Field(alias = 'wis')
    cha_: int = Field(alias = 'cha')
    save: dict[str,str]
    skill: dict[str,str]
    senses: list[str]
    passive: int
    resist: Optional[list[str|ResistancesModel]] = None
    immune: Optional[list[str|ImmunitiesModel]] = None
    vulnerable: Optional[list[str|VulnerabilitiesModel]] = None
    conditionImmune: Optional[list[str]] = None
    languages: list[str]
    cr: int
    spellcasting : Optional[list[SpellcastingModel]] = None
    trait: Optional[list[TraitModel]] = None
    action: Optional[list[ActionModel]] = None
    bonus: Optional[list[ActionModel]] = None
    legendary: Optional[list[ActionModel]] = None
    legendaryGroup : Optional[dict[str,str]] = None
    traitTags: list[str]
    senseTags: list[str]
    actionTags: list[str]
    languageTags: list[str]

    damageTags: list[str]
    damageTagsLegendary: Optional[list[str]] = None
    damageTagsSpell: Optional[list[str]] = None

    spellcastingTags: Optional[list[str]] = None

    conditionInflict: Optional[list[str]] = None
    conditionInflictLegendary: Optional[list[str]] = None
    conditionInflictSpell: Optional[list[str]] = None

    savingThrowForced: Optional[list[str]] = None
    savingThrowForcedLegendary: Optional[list[str]] = None
    savingThrowForcedSpell: Optional[list[str]] = None

    miscTags: list[str]
    hasToken: bool
    hasFluff: bool
    hasFluffImages: bool

    environment : Optional[list[str]] = None
    soundClip : Optional[dict[str,str]] = None
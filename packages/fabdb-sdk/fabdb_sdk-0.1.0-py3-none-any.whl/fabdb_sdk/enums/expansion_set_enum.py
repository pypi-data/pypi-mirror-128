# -*- coding: utf-8 -*-

from enum import Enum

from fabdb_sdk.helpers.enum_helper import EnumHelper


class ExpansionSetEnum(Enum, metaclass=EnumHelper):
    WTR = ("Welcome to Rath",)
    ARC = ("Arcane Rising",)
    CRU = ("Crucible of War",)
    MON = ("Monarch",)
    TOA = "Tales of Aria"

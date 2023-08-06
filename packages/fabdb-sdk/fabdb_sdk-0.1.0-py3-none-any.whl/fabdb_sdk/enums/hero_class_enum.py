# -*- coding: utf-8 -*-

from enum import Enum

from fabdb_sdk.helpers.enum_helper import EnumHelper


class HeroClassEnum(Enum, metaclass=EnumHelper):
    BRUTE = ("brute",)
    GUARDIAN = ("guardian",)
    MECHANOLOGIST = ("mechanologist",)
    NINJA = ("ninja",)
    RANGER = ("ranger",)
    RUNEBLADE = ("runeblade",)
    WARRIOR = ("warrior",)
    WIZARD = "wizard"

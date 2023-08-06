# -*- coding: utf-8 -*-

from enum import Enum

from fabdb_sdk.helpers.enum_helper import EnumHelper


class RarityEnum(Enum, metaclass=EnumHelper):
    COMMON = ("C",)
    RARE = ("R",)
    SUPER_RARE = "S"
    TOKEN = ("T",)
    LEGENDARY = ("L",)
    FABLE = ("F",)
    PROMO = "P"

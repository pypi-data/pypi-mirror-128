# -*- coding: utf-8 -*-


class Card:
    """Card Structure"""

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, value):
        self.__identifier = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def rarity(self):
        """docstring for rarity"""
        return self.__rarity

    @rarity.setter
    def rarity(self, value):
        self.__rarity = value

    @property
    def keywords(self):
        return self.__keywords

    @keywords.setter
    def keywords(self, value):
        self.__keywords = value

    @property
    def stats(self):
        return self.__stats

    @stats.setter
    def stats(self, value):
        self.__stats = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def flavour(self):
        return self.__flavour

    @flavour.setter
    def flavour(self, value):
        self.__flavour = value

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        self.__comments = value

    @property
    def banned(self):
        return self.__banned

    @banned.setter
    def banned(self, value):
        self.__banned = value

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def rullings(self):
        return self.__rullings

    @rullings.setter
    def rullings(self, value):
        self.__rullings = value

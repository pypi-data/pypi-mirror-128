# -*- coding: utf-8 -*-

from enum import EnumMeta


class EnumHelper(EnumMeta):
    def _contains(self, member):
        return member in self._member_map_ or member in set(
            map(lambda x: x.value, self._member_map_.values())
        )

    def is_valid(self, member):
        if self._contains(member):
            return True
        else:
            return False

#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from enum import Enum


class EntryPointRole(Enum):
    DEFAULT = "DEFAULT"
    MISSING_ENUM = ""

    @classmethod
    def _missing_(cls, value: object) -> "EntryPointRole":
        return cls.MISSING_ENUM

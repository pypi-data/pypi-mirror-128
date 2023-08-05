#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from enum import Enum


class FlowInstanceStatus(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    MISSING_ENUM = ""

    @classmethod
    def _missing_(cls, value: object) -> "FlowInstanceStatus":
        return cls.MISSING_ENUM

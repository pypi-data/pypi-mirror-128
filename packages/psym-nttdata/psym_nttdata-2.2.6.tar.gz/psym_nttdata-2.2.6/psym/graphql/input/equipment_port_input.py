#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from functools import partial
from ...config import custom_scalars, datetime
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional

from dataclasses_json import DataClassJsonMixin, config

from ..input.equipment_port_connection_input import EquipmentPortConnectionInput


@dataclass(frozen=True)
class EquipmentPortInput(DataClassJsonMixin):
    name: str
    connectedPorts: List[EquipmentPortConnectionInput]
    id: Optional[str] = None
    index: Optional[int] = None
    visibleLabel: Optional[str] = None
    portTypeID: Optional[str] = None
    bandwidth: Optional[str] = None

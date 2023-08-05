#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from ...config import custom_scalars, datetime
from gql_client.runtime.variables import encode_variables
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from functools import partial
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional
from time import perf_counter
from dataclasses_json import DataClassJsonMixin, config

# fmt: off
QUERY: List[str] = ["""
fragment EquipmentPositionDefinitionFragment on EquipmentPositionDefinition {
  id
  name
  index
  visibleLabel
}

"""]

@dataclass(frozen=True)
class EquipmentPositionDefinitionFragment(DataClassJsonMixin):
    id: str
    name: str
    index: Optional[int]
    visibleLabel: Optional[str]

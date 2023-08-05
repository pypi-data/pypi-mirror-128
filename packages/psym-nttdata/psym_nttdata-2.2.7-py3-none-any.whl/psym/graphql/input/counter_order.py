#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from functools import partial
from ...config import custom_scalars, datetime
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional

from dataclasses_json import DataClassJsonMixin, config

from gql_client.runtime.enum_utils import enum_field_metadata
from ..enum.counter_order_field import CounterOrderField
from ..enum.order_direction import OrderDirection


@dataclass(frozen=True)
class CounterOrder(DataClassJsonMixin):
    direction: OrderDirection = _field(metadata=enum_field_metadata(OrderDirection))
    field: Optional[CounterOrderField] = None

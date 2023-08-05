#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from functools import partial
from ...config import custom_scalars, datetime
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional

from dataclasses_json import DataClassJsonMixin, config

from gql_client.runtime.enum_utils import enum_field_metadata
from ..enum.trigger_type_id import TriggerTypeId

from ..input.block_u_i_representation_input import BlockUIRepresentationInput
from ..input.variable_expression_input import VariableExpressionInput


@dataclass(frozen=True)
class TriggerBlockInput(DataClassJsonMixin):
    cid: str
    triggerType: TriggerTypeId = _field(metadata=enum_field_metadata(TriggerTypeId))
    params: List[VariableExpressionInput]
    uiRepresentation: Optional[BlockUIRepresentationInput] = None

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

from ..input.edit_kqi_source_input import EditKqiSourceInput


# fmt: off
QUERY: List[str] = ["""
mutation editKqiSource($input: EditKqiSourceInput!) {
  editKqiSource(input: $input) {
    id
    name
  }
}

"""
]


class editKqiSource:
    @dataclass(frozen=True)
    class editKqiSourceData(DataClassJsonMixin):
        @dataclass(frozen=True)
        class KqiSource(DataClassJsonMixin):
            id: str
            name: str

        editKqiSource: KqiSource

    # fmt: off
    @classmethod
    def execute(cls, client: Client, input: EditKqiSourceInput) -> editKqiSourceData.KqiSource:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = client.execute(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editKqiSourceData.from_dict(response_text)
        return res.editKqiSource

    # fmt: off
    @classmethod
    async def execute_async(cls, client: Client, input: EditKqiSourceInput) -> editKqiSourceData.KqiSource:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = await client.execute_async(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editKqiSourceData.from_dict(response_text)
        return res.editKqiSource

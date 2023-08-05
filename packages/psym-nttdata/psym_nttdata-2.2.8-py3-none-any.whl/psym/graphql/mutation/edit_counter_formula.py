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

from ..input.edit_counter_formula_input import EditCounterFormulaInput


# fmt: off
QUERY: List[str] = ["""
mutation editCounterFormula($input: EditCounterFormulaInput!) {
  editCounterFormula(input: $input) {
    id
    mandatory
    formulaFk{id}
    counterFk{id}
  }
}
"""
]


class editCounterFormula:
    @dataclass(frozen=True)
    class editCounterFormulaData(DataClassJsonMixin):
        @dataclass(frozen=True)
        class CounterFormula(DataClassJsonMixin):
            @dataclass(frozen=True)
            class Formula(DataClassJsonMixin):
                id: str

            @dataclass(frozen=True)
            class Counter(DataClassJsonMixin):
                id: str

            id: str
            mandatory: bool
            formulaFk: Formula
            counterFk: Counter

        editCounterFormula: CounterFormula

    # fmt: off
    @classmethod
    def execute(cls, client: Client, input: EditCounterFormulaInput) -> editCounterFormulaData.CounterFormula:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = client.execute(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editCounterFormulaData.from_dict(response_text)
        return res.editCounterFormula

    # fmt: off
    @classmethod
    async def execute_async(cls, client: Client, input: EditCounterFormulaInput) -> editCounterFormulaData.CounterFormula:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = await client.execute_async(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editCounterFormulaData.from_dict(response_text)
        return res.editCounterFormula

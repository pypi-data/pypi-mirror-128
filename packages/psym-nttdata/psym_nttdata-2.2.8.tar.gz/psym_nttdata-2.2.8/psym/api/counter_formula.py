#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import counterFormula, formula, counter

from ..graphql.input.edit_counter_formula_input import EditCounterFormulaInput
from ..graphql.input.add_counter_formula_input import AddCounterFormulaInput
from ..graphql.mutation.add_counter_formula import addCounterFormula
from ..graphql.mutation.edit_counter_formula import editCounterFormula
from ..graphql.mutation.remove_counter_formula import removeCounterFormula
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_counter_formula(
    client: SymphonyClient,  mandatory: bool, counterFk: str,  formulaFK: str
) -> counterFormula:
   
    domain_input = AddCounterFormulaInput(
    mandatory=mandatory,
    counterFk=counterFk,
    formulaFk=formulaFK)

    result = addCounterFormula.execute(client, input=domain_input)

    return counterFormula(mandatory=result.mandatory,
    id=result.id,  
    counterFk=result.counterFk, 
    formulaFK=result.formulaFk)

def edit_ounter_formula(
    client: SymphonyClient,
    counterFormula: counterFormula,
    new_name: Optional[bool] = None,
    formulaFK: formula = None,
    counterFk: counter = None
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({True: new_name})
    if new_name is not None:
        editCounterFormula.execute(client, input=EditCounterFormulaInput(
        id=counterFormula.id, 
        mandatory=new_name,
        counterFk=counterFk,
        formulaFK=formulaFK,
        ))








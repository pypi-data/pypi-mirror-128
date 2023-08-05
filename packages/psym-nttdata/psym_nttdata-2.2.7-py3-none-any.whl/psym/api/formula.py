#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import formula

from ..graphql.input.edit_formula_input import EditFormulaInput
from ..graphql.input.add_formula_input import AddFormulaInput
from ..graphql.mutation.add_formula import addFormula
from ..graphql.mutation.edit_formula import editFormula
from ..graphql.mutation.remove_formula import removeFormula
from ..graphql.query.formulas import formulas
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_formula(
    client: SymphonyClient, textformula: str, status: bool,  techFk: str, networkTypeFk: str,  kpiFk: str
) -> formula:
   
    formula_input = AddFormulaInput(textFormula=textformula, 
    status=status, 
    techFk= techFk,
    networkTypeFk= networkTypeFk,
    kpiFk= kpiFk
   
   )
    result = addFormula.execute(client, input=formula_input)
    return formula(textFormula=result.textFormula, 
    id=result.id,  
    status=result.status, 
    techFk=result.techFk,
    networkTypeFk=result.networkTypeFk,
    kpiFk=result.kpiFk
)






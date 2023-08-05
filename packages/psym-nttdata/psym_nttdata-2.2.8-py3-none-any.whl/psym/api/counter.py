#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import CounterFamiliy, Vendor, counter

from ..graphql.input.edit_counter_input import EditCounterInput
from ..graphql.input.add_counter_input import AddCounterInput
from ..graphql.mutation.add_counter import addCounter
from ..graphql.mutation.edit_counter import editCounter
from ..graphql.mutation.remove_counter import removeCounter
from ..graphql.query.counters import counters
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_counter(
    client: SymphonyClient, name: str, externalID: str, networkManagerSystem: str,  counterFamilyFk: str, vendorFk: str
) -> counter:
   
    domain_input = AddCounterInput(name=name, 
    externalID=externalID,
    networkManagerSystem=networkManagerSystem, 
    counterFamily=counterFamilyFk,
    vendorFk=vendorFk)

    result = addCounter.execute(client, input=domain_input)

    return counter(name=result.name, id=result.id, 
    externalID=result.externalID, 
    networkManagerSystem=result.networkManagerSystem, 
    counterFamilyFk=result.counterFamily, 
    vendorFk=result.vendorFk)

def edit_counter(
    client: SymphonyClient,
    counter: counter,
    new_name: Optional[str] = None,
    externalID: str = None,
    networkManagerSystem: str = None,
    vendorFk: Vendor = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editCounter.execute(client, input=EditCounterInput(
        id=counter.id, 
        name=new_name,
        externalID=externalID,
        networkManagerSystem=networkManagerSystem,
        vendorFk=vendorFk,
        ))








#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import NetworkType, domain

from ..graphql.input.edit_network_type_input import EditNetworkTypeInput
from ..graphql.input.add_network_type_input import AddNetworkTypeInput
from ..graphql.mutation.add_network_type import addNetworkType
from ..graphql.mutation.edit_network_type import editNetworkType
from ..graphql.mutation.remove_network_type import removeNetworkType
from ..graphql.query.network_types import networkTypes
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_network_type(
    client: SymphonyClient, name: str
) -> NetworkType:
   
    network_type_input = AddNetworkTypeInput(name=name)
    result = addNetworkType.execute(client, input=network_type_input)
    return NetworkType(name=result.name, id=result.id)

def edit_network_type(
    client: SymphonyClient,
    network_type: NetworkType,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editNetworkType.execute(client, input=EditNetworkTypeInput(id=network_type.id, name=new_name))


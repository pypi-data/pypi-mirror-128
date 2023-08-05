#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.




from psym.client import SymphonyClient
from psym.common.data_class import KqiPerspective

from ..graphql.input.edit_kqi_perspective_input import EditKqiPerspectiveInput
from ..graphql.input.add_kqi_perspective_input import AddKqiPerspectiveInput
from ..graphql.input.edit_kqi_perspective_input import EditKqiPerspectiveInput
from ..graphql.mutation.add_kqi_perspective import addKqiPerspective
from ..graphql.mutation.edit_kqi_perspective import editKqiPerspective
from ..graphql.query.kqi_perspective import kqiPerspectives
from ..graphql.mutation.remove_kqi_perspective import removeKqiPerspective
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_kqi_perspective(
    client: SymphonyClient, name: str
) -> KqiPerspective:
   
    kqi_perspective_input = AddKqiPerspectiveInput(name=name)
    result = addKqiPerspective.execute(client, input=kqi_perspective_input)
    return KqiPerspective(name=result.name, id=result.id)


def edit_kqi_perspective(
    client: SymphonyClient,
    kqiperspective: KqiPerspective,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editKqiPerspective.execute(client, input=EditKqiPerspectiveInput(id=kqiperspective.id, name=new_name))


def get_kqi_perspectives(client: SymphonyClient) -> Iterator[KqiPerspective]:

    kqi_perspectives = kqiPerspectives.execute(client, first=PAGINATION_STEP)
    edges = kqi_perspectives.edges if kqi_perspectives else []
    while kqi_perspectives is not None and kqi_perspectives.pageInfo.hasNextPage:
        kqi_perspectives = kqiPerspectives.execute(
            client, after=kqi_perspectives.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if kqi_perspectives is not None:
            edges.extend(kqi_perspectives.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield KqiPerspective(
                id=node.id,
                name=node.name,
            )


def delete_kqi_perspective(client: SymphonyClient, id: str) -> None:
    removeKqiPerspective.execute(client, id=id)




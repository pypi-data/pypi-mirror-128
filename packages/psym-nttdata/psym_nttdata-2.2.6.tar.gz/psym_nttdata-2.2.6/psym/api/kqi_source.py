#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.




from psym.client import SymphonyClient
from psym.common.data_class import KqiSource

from ..graphql.input.edit_kqi_source_input import EditKqiSourceInput
from ..graphql.input.add_kqi_source_input import AddKqiSourceInput
from ..graphql.input.edit_kqi_source_input import EditKqiSourceInput
from ..graphql.mutation.add_kqi_source import addKqiSource
from ..graphql.mutation.edit_kqi_source import editKqiSource
from ..graphql.query.kqi_source import kqiSources
from ..graphql.mutation.remove_kqi_source import removeKqiSource
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_kqi_source(
    client: SymphonyClient, name: str
) -> KqiSource:
   
    kqi_source_input = AddKqiSourceInput(name=name)
    result = addKqiSource.execute(client, input=kqi_source_input)
    return KqiSource(name=result.name, id=result.id)


def edit_kqi_source(
    client: SymphonyClient,
    kqisource: KqiSource,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editKqiSource.execute(client, input=EditKqiSourceInput(id=kqisource.id, name=new_name))


def get_kqi_sources(client: SymphonyClient) -> Iterator[KqiSource]:

    kqi_sources = kqiSources.execute(client, first=PAGINATION_STEP)
    edges = kqi_sources.edges if kqi_sources else []
    while kqi_sources is not None and kqi_sources.pageInfo.hasNextPage:
        kqi_sources = kqiSources.execute(
            client, after=kqi_sources.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if kqi_sources is not None:
            edges.extend(kqi_sources.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield KqiSource(
                id=node.id,
                name=node.name,
            )


def delete_kqi_source(client: SymphonyClient, id: str) -> None:
    removeKqiSource.execute(client, id=id)




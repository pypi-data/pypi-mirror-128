#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import Kpi, domain, KpiCategory

from ..graphql.input.edit_kpi_input import EditKpiInput
from ..graphql.input.add_kpi_input import AddKpiInput
from ..graphql.mutation.add_kpi import addKpi
from ..graphql.mutation.edit_kpi import editKpi
from ..graphql.mutation.remove_kpi import removeKpi
from ..graphql.query.kpis import kpis
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_kpi(
    client: SymphonyClient, name: str, description: str, status: bool, domainId: str, kpiCategoryId: str
) -> domain:
   
    domain_input = AddKpiInput(name=name, description=description,
    status=status, 
    domainFk=domainId,
    kpiCategoryFK=kpiCategoryId)

    result = addKpi.execute(client, input=domain_input)

    return Kpi(name=result.name, id=result.id, 
    description=result.description, 
    status=result.status, 
    domainFK=result.domainFk, 
    kpiCategoryFK=result.kpiCategoryFK)

def edit_kpi(
    client: SymphonyClient,
    KPI: Kpi,
    new_name: Optional[str] = None,
    description: str = None,
    status: bool = None,
    domainId: domain = None,
    kpiCategoryId: KpiCategory = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editKpi.execute(client, input=EditKpiInput(id=KPI.id, 
        name=new_name,
        description=description,
        status= status,
        domainFk=domainId,
        kpiCategoryFK=kpiCategoryId
        ))








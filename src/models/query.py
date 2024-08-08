
from typing import List
import strawberry

from ..services.query_service import QueryService
from ..services.query_service_csv_impl import QueryServiceCsvImpl
from ..models.item import Item

@strawberry.type
class Query:
    @strawberry.field
    def get_items(self) -> List[Item]:
        service: QueryService = QueryServiceCsvImpl()
        return service.get_all()

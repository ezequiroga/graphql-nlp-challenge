
from typing import Dict, List
import pandas as pd
import os

from ..utils.cons import Cons
from .query_service import QueryService
from ..models.item import Item
from ..config.envs import Envs

class QueryServiceCsvImpl(QueryService):

    def __init__(self):
        self.df = pd.read_csv(Envs.get_csv_file_path())

        self.df = self.df.drop_duplicates()
        self.df = self.df[self.df['desc_ga_sku_producto_1'].str.lower() != 'no aplica']
        self.df = self.df.fillna('')

    def __map_columns(self, row: Dict[str, any]) -> Dict[str, any]:
        valid_fields = {Cons.COLUMN_MAPPING.get(k, k): v for k, v in row.items() if k in Cons.COLUMN_MAPPING}
        for key in Cons.COLUMN_MAPPING.values():
            if key not in valid_fields:
                valid_fields[key] = None
        return valid_fields
    
    def get_all(self) -> List[Item]:
        items = [self.__map_columns(item) for item in self.df.to_dict(orient="records")]
        return [Item(**item) for item in items]

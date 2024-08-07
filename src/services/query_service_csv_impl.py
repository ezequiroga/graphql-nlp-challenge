
from typing import Dict, List
import pandas as pd

from .query_service import QueryService
from ..models.item import Item

class QueryServiceCsvImpl(QueryService):

    COLUMN_MAPPING = {
        "id_tie_fecha_valor": "date",
        "id_cli_cliente": "client_id",
        "desc_ga_sku_producto_1": "sku",
        "desc_ga_cod_producto": "product_code",
        "desc_ga_nombre_producto_1": "product_name",
        "desc_ga_marca_producto": "brand",
        "desc_categoria_producto": "product_category",
        "desc_categoria_prod_principal": "main_product_category",
        "fc_producto_cant": "product_quantity",
        "fc_detalle_producto_cant": "product_detail_quantity",
        "fc_ingreso_producto_monto": "product_income_amount",
        "fc_agregado_carrito_cant": "added_to_cart_quantity",
        "fc_retirado_carrito_cant": "removed_from_cart_quantity",
        "flag_pipol": "flag_pipol",
    }

    def __init__(self):
        self.df = pd.read_csv('/Users/ezequielquiroga/Documents/challenge-coding/src/data.csv')

        self.df = self.df.drop_duplicates()
        self.df = self.df[self.df['desc_ga_sku_producto_1'].str.lower() != 'no aplica']
        self.df = self.df.fillna('')

    def __map_columns(self, row: Dict[str, any]) -> Dict[str, any]:
        valid_fields = {self.COLUMN_MAPPING.get(k, k): v for k, v in row.items() if k in self.COLUMN_MAPPING}
        for key in self.COLUMN_MAPPING.values():
            if key not in valid_fields:
                valid_fields[key] = None
        return valid_fields
    
    def get_all(self) -> List[Item]:
        items = [self.__map_columns(item) for item in self.df.to_dict(orient="records")]
        return [Item(**item) for item in items]

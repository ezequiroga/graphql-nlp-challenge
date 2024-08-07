import pandas as pd
import strawberry
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from typing import List, Dict, NewType
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

df = pd.read_csv('data.csv')

df = df.drop_duplicates()
df = df[df['desc_ga_sku_producto_1'].str.lower() != 'no aplica']
df = df.fillna('')

Integer = strawberry.scalar(
    NewType("Integer", int),
    serialize=lambda v: int(v) if v is not None and not v == '' else 0,
    parse_value=lambda v: str(v),
)

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

@strawberry.type
class Item:
    date: str
    client_id: int
    sku: str
    product_code: int
    product_name: str
    brand: str
    product_category: str
    main_product_category: str
    product_quantity: int
    product_detail_quantity: int
    product_income_amount: float
    added_to_cart_quantity: int
    removed_from_cart_quantity: int
    flag_pipol: int

def map_columns(row: Dict[str, any]) -> Dict[str, any]:
    valid_fields = {COLUMN_MAPPING.get(k, k): v for k, v in row.items() if k in COLUMN_MAPPING}
    for key in COLUMN_MAPPING.values():
        if key not in valid_fields:
            valid_fields[key] = None
    return valid_fields

@strawberry.type
class Query:
    @strawberry.field
    def get_items(self) -> List[Item]:
        items = [map_columns(item) for item in df.to_dict(orient="records")]
        return [Item(**item) for item in items]

schema = strawberry.Schema(query=Query, scalar_overrides={int: Integer})

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

class DocumentationResponse(BaseModel):
    documentation: dict

@app.get("/documentation", response_model=DocumentationResponse)
def get_documentation():
    return JSONResponse(content=get_openapi(title="GraphQL API", version="1.0.0", routes=app.routes))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

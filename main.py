import pandas as pd
import strawberry
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from typing import List, Dict
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

df = pd.read_csv('data.csv')

df = df[df['desc_ga_sku_producto_1'].str.lower() != 'no aplica']

COLUMN_MAPPING = {
    "desc_ga_sku_producto_1": "sku",
}

@strawberry.type
class Item:
    SKU: str

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

schema = strawberry.Schema(query=Query)

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

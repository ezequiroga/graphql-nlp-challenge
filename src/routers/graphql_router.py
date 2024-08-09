from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
import strawberry
from strawberry.fastapi import GraphQLRouter

from ..types.custom_integer import Integer
from ..models.query import Query


schema = strawberry.Schema(query=Query, scalar_overrides={int: Integer})
graphql_app = GraphQLRouter(schema, include_in_schema=False)

router = APIRouter()

@router.get("/graphql-docs",
            summary="GraphQL Documentation",
            description="This endpoint allow the user to see the GraphQL fields to be used.",
            response_class=PlainTextResponse
            )
async def graphql_docs():
    return f"""
The GraphQL endpoint is /graphql. You can use the following query to get the products:

{schema.as_str()}
    """

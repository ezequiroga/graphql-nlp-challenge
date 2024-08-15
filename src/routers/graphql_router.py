from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
import strawberry
from strawberry.fastapi import GraphQLRouter

from ..config.auth import get_current_user
from ..types.custom_integer import Integer
from ..models.query import Query


schema = strawberry.Schema(query=Query, scalar_overrides={int: Integer})
graphql_app = GraphQLRouter(schema, include_in_schema=False)

async def secure_graphql(request: Request, user: dict = Depends(get_current_user)):
    # log user activity
    return await graphql_app.handle_graphql(request=request)

graphql_app.handle_graphql = secure_graphql


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

import strawberry
from strawberry.fastapi import GraphQLRouter

from ..types.custom_integer import Integer
from ..models.query import Query


schema = strawberry.Schema(query=Query, scalar_overrides={int: Integer})
graphql_app = GraphQLRouter(schema)

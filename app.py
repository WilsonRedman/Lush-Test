from strawberry.fastapi import GraphQLRouter
from schema import task_schema
from fastapi import FastAPI

graphql_app = GraphQLRouter(task_schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

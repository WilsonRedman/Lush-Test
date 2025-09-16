from sqlalchemy import create_engine, text
from graphql import GraphQLError
import strawberry
import typing

engine = create_engine("sqlite:///test_db.db")

@strawberry.type
class Task:
    id: int
    title: str
    completed: bool
    created_at: str
    updated_at: str

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, search: typing.Optional[str] = "") -> typing.List[Task]:
        with engine.connect() as conn:
            result = conn.execute(text("""SELECT * FROM tasks WHERE title LIKE :search"""), {"search": f"%{search}%"})
            
            tasks = [
                Task(
                    id = row.id,
                    title = row.title,
                    completed = bool(row.completed),
                    created_at = row.created_at,
                    updated_at = row.updated_at
                )
                for row in result
            ]
            return tasks
    
    @strawberry.field
    def task(self, id: int) -> typing.Optional[Task] | None:
        with engine.connect() as conn:
            result = conn.execute(text("""SELECT * FROM tasks WHERE id = :id"""), {"id": id}).fetchone()
            
            if result:
                return Task(
                    id = result.id,
                    title = result.title,
                    completed = bool(result.completed),
                    created_at = result.created_at,
                    updated_at = result.updated_at
                )
            else:
                raise GraphQLError(f"Task not found with ID: {id}")
            
    @strawberry.field
    def incomplete_tasks(self) -> typing.Optional[typing.List[Task]] | None:
        with engine.connect() as conn:
            result = conn.execute(text("""SELECT * FROM tasks WHERE completed = 0"""))
            
            tasks = [
                Task(
                    id = row.id,
                    title = row.title,
                    completed = bool(row.completed),
                    created_at = row.created_at,
                    updated_at = row.updated_at
                )
                for row in result
            ]
            if tasks:
                return tasks
            else:
                raise GraphQLError("No incomplete tasks found")
            
    @strawberry.field     
    def recently_completed_tasks(self) -> typing.Optional[typing.List[Task]] | None:
        with engine.connect() as conn:
            result = conn.execute(text(""" SELECT * FROM tasks 
                                            WHERE completed = 1 
                                            ORDER BY updated_at DESC 
                                            LIMIT 3"""))
            
            tasks = [
                Task(
                    id = row.id,
                    title = row.title,
                    completed = bool(row.completed),
                    created_at = row.created_at,
                    updated_at = row.updated_at
                )
                for row in result
            ]
            if tasks:
                return tasks
            else:
                raise GraphQLError("No completed tasks found")
            
            
            
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(self, title: str) -> Task:
        with engine.begin() as conn:
            conn.execute(text("""INSERT INTO tasks (title) VALUES (:title)"""), {"title": title})

            task = conn.execute(text("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")).fetchone()
            return Task(
                id = task.id,
                title = task.title,
                completed = bool(task.completed),
                created_at = task.created_at,
                updated_at = task.updated_at
            )
    
    @strawberry.mutation
    def toggle_task(self, id: int) -> typing.Optional[Task] | None:
        with engine.begin() as conn:
            conn.execute(text("""   UPDATE tasks SET completed = CASE completed WHEN 1 THEN 0 ELSE 1 END, 
                                    updated_at = CURRENT_TIMESTAMP
                                    WHERE id = :id"""), {"id": id})

            task = conn.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": id}).fetchone()
            if task:
                return Task(
                    id = task.id,
                    title = task.title,
                    completed = bool(task.completed),
                    created_at = task.created_at,
                    updated_at = task.updated_at
                )
            else:
                raise GraphQLError(f"Task not found with ID: {id}")
            
    @strawberry.mutation
    def delete_task(self, id: int) -> typing.Optional[Task] | None:
        with engine.begin() as conn:
            task = conn.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": id}).fetchone()
            if task:
                conn.execute(text("DELETE FROM tasks WHERE id = :id"), {"id": id})
                return Task(
                    id = task.id,
                    title = task.title,
                    completed = bool(task.completed),
                    created_at = task.created_at,
                    updated_at = task.updated_at
                )
            else:
                raise GraphQLError(f"Task not found with ID: {id}")


task_schema = strawberry.Schema(query=Query, mutation=Mutation)
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, DateTime, func, MetaData
import time

engine = create_engine("sqlite:///test_db.db")
metadata = MetaData()

task_table = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("completed", Boolean, default=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
)

metadata.create_all(engine)

dummy_tasks = ["Task 1", "Task 2", "Task 3"]

with engine.begin() as conn:
    for task in dummy_tasks:
        conn.execute(task_table.insert().values(title=task))
        time.sleep(1)
        ## Different creation times for dummy tasks

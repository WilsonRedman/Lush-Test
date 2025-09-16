# Lush-Test

## Setup

- Create local venv.
- Execute `pip install -r requirements.txt`.
- Run `create_db.py` to create local database and dummy data.
- Run `app.py` to run the FastAPI Server on localhost.
- Load [localhost server](http://localhost:8000/graphql) on provided link to run queries and mutations

## Queries and Mutations
### Queries:
- `tasks(search: String)` Returns all tasks, optionally filter by title.
- `task(id: ID!)` Returns a single task by ID.
- `incompleteTasks` Returns all incomplete tasks.
- `recentlyCompletedTasks` Returns three most recently completed tasks

### Mutations
- `addTask(title: String!)` Adds a task, auto creating ID, completed as false, and timestamps.
- `toggleTask(id: ID!)` Toggles the completion of the task with given ID.
- `deleteTask(id: ID!)` Deletes the task with given ID.

## Additions
- Added incompleteTasks query dispalying all tasks that need to be completed.
- Added recentlyCompletedTasks query displaying the three most recently completed tasks in the database.

## Error Handling
Currently errors are handled by raising GraphQL errors. This returns null and also provides a message of what the issue is. More complex errors (when dealing with a lot of fields) could be handled similarly by checking different inputs.

Current inputs are formatted in a way to prevent SQL injections.
# To-Do-API
ToDo API is an API for task management. Users can create, view, update and delete tasks, as well as assign permissions to other users.

## Functions

- Sign up and sign in
- Create, view, update and delete tasks
- Assign and revoke permissions to tasks for other users
  - Permissions: Read, Update

## Tech Stack

- Language: Python
- DBMS: PostgreSQL
- Framework: Django
- Django REST Framework
- Simple JWT for authentication

## Endpoints API

### Sign up

- **POST /api/register/**

    ```json
    {
        "username": "newuser",
        "password": "newpassword"
    }
    ```

### Sign in

- **POST /api/login/**

    ```json
    {
        "username": "newuser",
        "password": "newpassword"
    }
    ```

    **Response:**

    ```json
    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }
    ```

### Tasks

- **GET /api/tasks/**: Get a list of tasks available to the current user
- **POST /api/tasks/**: Create a new task

    ```json
    {
        "title": "New Task",
        "description": "This is a new task"
    }
    ```

- **GET /api/tasks/{id}/**: Get task info
- **PUT /api/tasks/{id}/**: Update the task

    ```json
    {
        "title": "Updated Task",
        "description": "This task has been updated"
    }
    ```

- **DELETE /api/tasks/{id}/**: Delete the task

### Права на задачи

- **GET /api/permissions/**: Get a list of permissions for the current user
- **POST /api/permissions/**: Grant task rights to another user

    ```json
    {
        "task": "New Task",
        "user": "anotheruser",
        "permission": "read"
    }
    ```

- **DELETE /api/permissions/{id}/**: Revoke rights

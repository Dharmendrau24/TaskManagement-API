# Task Management API

A production-style REST API built with **Python, FastAPI, PostgreSQL, SQLAlchemy, JWT authentication, and pytest**.

The project demonstrates authenticated task management with user isolation, filtering, searching, sorting, pagination, validation, and automated API testing.

## Tech Stack

* Python 3.13
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* pwdlib
* pytest
* HTTPX
* Docker-ready architecture

## Features

### Authentication

* User registration
* User login
* JWT-based authentication
* Authenticated user verification
* Password hashing
* Invalid username/password handling
* Invalid/expired token handling

### Task Management

* Create tasks
* Get authenticated user's tasks
* Get a single task
* Update tasks
* Delete tasks
* User-specific task access

### Task Filtering

* Filter by priority
* Filter by completion status
* Search tasks by title

### Sorting

Tasks can be sorted by:

* Created date
* Updated date
* Due date
* Title
* Priority

Supported sort orders:

* Ascending
* Descending

### Pagination

The API supports:

* `skip`
* `limit`
* Page information
* Previous/next page information

Example:

```text
GET /tasks?skip=0&limit=10
```

## Project Structure

```text
task_management_app/
│
├── src/
│   ├── tasks/
│   │   ├── controller.py
│   │   ├── dtos.py
│   │   ├── models.py
│   │   └── router.py
│   │
│   ├── user/
│   │   ├── controller.py
│   │   ├── dtos.py
│   │   ├── models.py
│   │   └── router.py
│   │
│   └── utils/
│       ├── db.py
│       ├── helpers.py
│       └── settings.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_main.py
│
├── .env.example
├── .gitignore
├── main.py
└── README.md
```

## Requirements

Make sure you have installed:

* Python 3.13+
* PostgreSQL
* Git

## Installation

Clone the repository:

```bash
git clone <https://github.com/Dharmendrau24/TaskManagement-API>
cd task_management_app
```

Create a virtual environment:

### Windows

```powershell
python -m venv env
```

Activate it:

```powershell
.\env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root.

Use `.env.example` as a template:

```env
DB_CONNECTION="postgresql://postgres:YOUR_PASSWORD@localhost:5432/myDb"
SECRET_KEY="YOUR_SECRET_KEY"
ALGORITHM="HS256"
EXP_TIME=30
```

Do not commit your `.env` file to GitHub.

## Database Setup

Create a PostgreSQL database:

```text
myDb
```

Update the database connection in `.env` according to your PostgreSQL configuration.

The application creates the required database tables using SQLAlchemy.

## Run the API

Start the development server:

```powershell
python -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## API Endpoints

### User

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| POST   | `/user/register` | Register a new user    |
| POST   | `/user/login`    | Login and receive JWT  |
| GET    | `/user/is_auth`  | Get authenticated user |

### Tasks

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| POST   | `/tasks`           | Create a task       |
| GET    | `/tasks`           | Get user's tasks    |
| GET    | `/tasks/{task_id}` | Get a specific task |
| PUT    | `/tasks/{task_id}` | Update a task       |
| DELETE | `/tasks/{task_id}` | Delete a task       |

## Example Task

Create a task:

```json
{
    "title": "Learn FastAPI Testing",
    "description": "Write authenticated API tests",
    "is_completed": false,
    "priority": "high",
    "due_date": null
}
```

## Testing

The project uses **pytest** for automated API testing.

A separate PostgreSQL database is used for tests:

```text
myDb_test
```

Run all tests:

```powershell
python -m pytest -v
```

Current test coverage includes:

* Authentication
* Authorization
* Task CRUD
* User isolation
* Validation
* Filtering
* Searching
* Sorting
* Pagination

Current test result:

```text
24 passed
```

## Security

The application implements:

* Password hashing
* JWT authentication
* User-specific task access
* Protected task endpoints
* Environment-based configuration

Sensitive credentials and secrets should always be stored in `.env` and excluded from version control.

## Future Improvements

Potential improvements include:

* Alembic database migrations
* Refresh tokens
* Role-based authorization
* Better exception handling
* Structured logging
* Docker and Docker Compose
* CI/CD with GitHub Actions
* API rate limiting
* More comprehensive test coverage
* PostgreSQL transaction management
* Production deployment

## Author

**Dharmendra Upadhyay**

Python Backend Engineer

Focus:

* Python
* FastAPI
* Django
* PostgreSQL
* SQLAlchemy
* Celery
* Redis
* REST APIs
* Backend System Design

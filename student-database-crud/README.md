# Student Database CRUD API

A Python backend internship project built with **FastAPI** and **SQLite**. It supports creating, listing, filtering, retrieving, updating, and deleting student records. An optional local Ollama endpoint can answer questions using a limited set of database records.

## Features

- Full CRUD operations for student records
- SQLite persistence; no separate database server required
- Input validation with Pydantic
- Unique email constraint and useful HTTP errors
- Filter students by name, course, and date of birth
- Pagination with `limit` and `offset`
- Interactive Swagger API documentation
- Optional local AI endpoint using Ollama
- Parameterized SQL queries to reduce SQL injection risk

## Technology stack

- Python 3.10+
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Optional: Ollama with `llama3.2:1b`

## Project structure

```text
student-database-crud/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_api.py
```

The SQLite file (`students.db`) is created automatically on startup and is intentionally excluded from Git.

## Prerequisites

1. Install Python 3.10 or newer.
2. Install Git if you plan to publish the project on GitHub.
3. Use a terminal in the project directory.

Check Python:

```bash
python --version
```

On some systems, use `python3` instead of `python`.

## Installation

### Windows (PowerShell or Command Prompt)

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn main:app --reload
```

Open these addresses in your browser:

- API home: http://127.0.0.1:8000/
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- Alternative API documentation: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

Use `/docs` to test the endpoints without installing a separate API client.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List and filter students |
| `GET` | `/students/{student_id}` | Retrieve one student |
| `PUT` | `/students/{student_id}` | Update supplied student fields |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `POST` | `/ai/ask?question=...` | Optional Ollama question-answering |

### Create a student

Send a `POST` request to `/students` with this JSON:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2005-04-17",
  "email": "aarav.demo@example.com",
  "phone": "+91 9876543210",
  "course": "BCA",
  "address": "Demo Address, India",
  "enrollment_date": "2025-08-01"
}
```

The email and date formats are validated. `enrollment_date` defaults to today's date if omitted. Use fictional data only.

### List and filter students

```bash
curl "http://127.0.0.1:8000/students"
curl "http://127.0.0.1:8000/students?name=Aarav"
curl "http://127.0.0.1:8000/students?course=BCA"
curl "http://127.0.0.1:8000/students?born_after=2005-01-01"
curl "http://127.0.0.1:8000/students?limit=20&offset=0"
```

### Get one student

```bash
curl "http://127.0.0.1:8000/students/1"
```

### Update a student

Send a `PUT` request to `/students/1`:

```json
{
  "course": "BCA - AI",
  "phone": "+91 9000000000"
}
```

Only supplied fields are changed.

### Delete a student

```bash
curl -X DELETE "http://127.0.0.1:8000/students/1"
```

## Expected error handling

- `201 Created`: student created
- `200 OK`: successful read, update, or delete
- `404 Not Found`: student ID does not exist
- `409 Conflict`: email already exists
- `422 Unprocessable Entity`: invalid request data
- `400 Bad Request`: empty update or other invalid operation
- `503 Service Unavailable`: optional Ollama service is unavailable

## Run tests

With dependencies installed, run:

```bash
pytest -v
```

Tests use a temporary SQLite database and do not alter your local project database.

## Optional local AI extension (Ollama)

This feature is not required for the assignment. Install Ollama from its official website, then run:

```bash
ollama pull llama3.2:1b
ollama run llama3.2:1b
```

Keep Ollama running, start the FastAPI server in another terminal, then send a request:

```bash
curl -X POST "http://127.0.0.1:8000/ai/ask?question=How%20many%20students%20are%20there%3F"
```

The endpoint fetches a restricted set of fields from SQLite and passes those records to the model. The model does not execute SQL. Since language models can still make mistakes, verify numeric answers against the database before relying on them. The AI endpoint intentionally excludes contact information.

## Publish to GitHub

1. Create a new **public** repository on GitHub, for example `student-database-crud`.
2. Do not initialize the GitHub repository with another README if you already have this project README.
3. Open a terminal in the project folder and run:

```bash
git init
git add .
git status
git commit -m "Build Student Database CRUD API with FastAPI and SQLite"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/student-database-crud.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Review `git status` before committing. Do not upload `.venv`, `students.db`, secrets, or real student information.

## Demonstration checklist

- [ ] Start the API successfully
- [ ] Create a sample student
- [ ] List all students
- [ ] Filter students by name or course
- [ ] Retrieve a single student
- [ ] Update a student
- [ ] Delete a student
- [ ] Verify a missing ID returns `404`
- [ ] Verify a duplicate email returns `409`
- [ ] Run `pytest -v`
- [ ] Optional: demonstrate the Ollama endpoint

## Architecture overview

```text
Client / Swagger UI
        |
        v
FastAPI routes and Pydantic validation
        |
        v
Parameterized SQLite queries
        |
        v
students.db (persistent local database)

Optional AI route:
Question -> restricted student fields from SQLite -> local Ollama -> answer
```

## Internship submission note

This repository is a learning project for the EWB EDU TECH PVT. LTD. Python Backend Development assignment. Review the code, run the tests, and be ready to explain each endpoint before submitting it.

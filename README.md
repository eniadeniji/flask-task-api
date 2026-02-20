# Flask Task API

## Description
A simple RESTful API built with Flask that allows users to manage tasks.
This project demonstrates CRUD operations using a JSON file for persistence.

## Features
- GET /tasks → Retrieve all tasks
- POST /tasks → Add a new task
- PUT /tasks/<id> → Update a task
- DELETE /tasks/<id> → Delete a task
- JSON file persistence
- Error handling for invalid input

## How to Run
1. Install dependencies:
   pip install flask

2. Run the server:
   python app.py

3. Open in browser:
   http://127.0.0.1:5000/

## Example Endpoints
- GET: /tasks
- POST: /tasks
- PUT: /tasks/1
- DELETE: /tasks/1

## Tech Stack
- Python
- Flask
- SQLite (Database)
- REST API Architecture

## Features
- Full CRUD API (Create, Read, Update, Delete)
- SQLite database persistence
- RESTful endpoints
- Error handling and validation
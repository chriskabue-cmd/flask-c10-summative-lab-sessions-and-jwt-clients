# Productivity API

## Setup
pipenv install
pipenv shell
flask db upgrade
python seed.py
flask run

## Features
- User authentication (session-based)
- CRUD Notes API
- User-owned data protection
- Pagination

## Endpoints

POST /signup
POST /login
DELETE /logout
GET /me

GET /notes?page=1
POST /notes
PATCH /notes/<id>
DELETE /notes/<id>
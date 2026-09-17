# Student Management System

A beginner-friendly college CRUD project built with Python Flask, SQLite, HTML, CSS, and JavaScript.

## Features

- Add, view, edit, and delete student records
- Search by name, register number, email, or department
- Client-side and server-side form validation
- REST API with JSON responses
- SQLite database created automatically on first run
- Responsive interface for desktop and mobile screens

## Project structure

```text
StudentManagement/
├── app.py
├── database.db
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md
```

## Installation and running

Open PowerShell in this folder and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open <http://127.0.0.1:5000> in a browser.

If PowerShell blocks activation, run this once in an Administrator PowerShell or use Command Prompt instead:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Command Prompt activation:

```bat
venv\Scripts\activate
```

## REST API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/students` | Return all students |
| `GET` | `/api/students/<id>` | Return one student |
| `GET` | `/api/students?search=term` | Search student records |
| `POST` | `/api/students` | Add a student |
| `PUT` | `/api/students/<id>` | Update a student |
| `DELETE` | `/api/students/<id>` | Delete a student |

Example JSON for `POST` and `PUT`:

```json
{
  "name": "Ananya Sharma",
  "register_number": "CS2024001",
  "email": "ananya@college.edu",
  "department": "Computer Science",
  "year": 2
}
```

The `year` value must be a number from 1 to 6. Register numbers and email addresses must be unique.
Screenshots of Website
<img width="907" height="566" alt="image" src="https://github.com/user-attachments/assets/41f8834d-d822-4674-91ac-75944932522a" />
Screenshots of postman testing
<img width="960" height="564" alt="Screenshot 2026-09-16 212107" src="https://github.com/user-attachments/assets/f2691330-ef36-455c-ac45-0330a7236869" />
<img width="960" height="564" alt="Screenshot 2026-09-16 212011" src="https://github.com/user-attachments/assets/fec32f0e-91bd-4f0d-9fe7-0e120b22598b" />
<img width="960" height="564" alt="Screenshot 2026-09-16 211936" src="https://github.com/user-attachments/assets/f4edd634-a22f-4d93-aced-9026212622c9" />




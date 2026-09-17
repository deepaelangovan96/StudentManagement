from pathlib import Path
import sqlite3

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
DATABASE = Path(__file__).with_name("database.db")
REQUIRED_FIELDS = ("name", "register_number", "email", "department", "year")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_number TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year INTEGER NOT NULL CHECK (year BETWEEN 1 AND 6)
        )
        """
    )
    connection.commit()
    connection.close()


def student_to_dict(student):
    return dict(student)


def validate_student_data(data):
    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    missing_fields = [field for field in REQUIRED_FIELDS if not str(data.get(field, "")).strip()]
    if missing_fields:
        return f"Missing required fields: {', '.join(missing_fields)}."

    name = str(data["name"]).strip()
    register_number = str(data["register_number"]).strip()
    email = str(data["email"]).strip()
    department = str(data["department"]).strip()

    if len(name) < 2:
        return "Name must contain at least 2 characters."
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Please enter a valid email address."

    try:
        year = int(data["year"])
    except (TypeError, ValueError):
        return "Year must be a number between 1 and 6."

    if year < 1 or year > 6:
        return "Year must be a number between 1 and 6."

    return {
        "name": name,
        "register_number": register_number,
        "email": email,
        "department": department,
        "year": year,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/students", methods=["GET"])
def get_students():
    search = request.args.get("search", "").strip()
    connection = get_db_connection()

    if search:
        pattern = f"%{search}%"
        students = connection.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ? OR register_number LIKE ?
               OR email LIKE ? OR department LIKE ?
            ORDER BY id DESC
            """,
            (pattern, pattern, pattern, pattern),
        ).fetchall()
    else:
        students = connection.execute("SELECT * FROM students ORDER BY id DESC").fetchall()

    connection.close()
    return jsonify([student_to_dict(student) for student in students])


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    connection = get_db_connection()
    student = connection.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    connection.close()

    if student is None:
        return jsonify({"error": "Student not found."}), 404
    return jsonify(student_to_dict(student))


@app.route("/api/students", methods=["POST"])
def create_student():
    data = validate_student_data(request.get_json(silent=True))
    if isinstance(data, str):
        return jsonify({"error": data}), 400

    connection = get_db_connection()
    try:
        cursor = connection.execute(
            """
            INSERT INTO students (name, register_number, email, department, year)
            VALUES (:name, :register_number, :email, :department, :year)
            """,
            data,
        )
        connection.commit()
        student = connection.execute("SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        connection.close()
        return jsonify({"error": "Register number or email already exists."}), 409

    connection.close()
    return jsonify(student_to_dict(student)), 201


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = validate_student_data(request.get_json(silent=True))
    if isinstance(data, str):
        return jsonify({"error": data}), 400

    connection = get_db_connection()
    existing_student = connection.execute("SELECT id FROM students WHERE id = ?", (student_id,)).fetchone()
    if existing_student is None:
        connection.close()
        return jsonify({"error": "Student not found."}), 404

    try:
        connection.execute(
            """
            UPDATE students
            SET name = :name, register_number = :register_number,
                email = :email, department = :department, year = :year
            WHERE id = :id
            """,
            {**data, "id": student_id},
        )
        connection.commit()
        student = connection.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    except sqlite3.IntegrityError:
        connection.close()
        return jsonify({"error": "Register number or email already exists."}), 409

    connection.close()
    return jsonify(student_to_dict(student))


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    connection = get_db_connection()
    cursor = connection.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"message": "Student deleted successfully."})


@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found."}), 404
    return error


@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({"error": "An unexpected server error occurred."}), 500


init_database()


if __name__ == "__main__":
    app.run(debug=True)

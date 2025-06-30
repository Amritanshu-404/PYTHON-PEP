from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = "db.sqlite3"


# ✅ Initialize database and table
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()
    print("✅ Database initialized with 'employee' table")


# ✅ Create a new employee
@app.route("/employee", methods=["POST"])
def create_employee():
    try:
        data = request.get_json(force=True)
        name = data["name"]
        salary = data["salary"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employee (name, salary) VALUES (?, ?)", (name, salary)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Employee created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Get all employees
@app.route("/employees", methods=["GET"])
def get_all_employees():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee")
    rows = cursor.fetchall()
    conn.close()

    employees = [{"id": row[0], "name": row[1], "salary": row[2]} for row in rows]
    return jsonify(employees)


# ✅ Get a single employee by ID
@app.route("/employee/<int:id>", methods=["GET"])
def get_employee(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"id": row[0], "name": row[1], "salary": row[2]})
    return jsonify({"message": "Employee not found"}), 404


# ✅ Update employee
@app.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):
    try:
        data = request.get_json(force=True)
        name = data["name"]
        salary = data["salary"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE employee SET name = ?, salary = ? WHERE id = ?", (name, salary, id)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Employee updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Delete employee
@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Employee deleted successfully"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

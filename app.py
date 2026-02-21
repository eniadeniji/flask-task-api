from flask import Flask, request, jsonify
import sqlite3
from database import init_db, get_connection

app = Flask(__name__)
init_db()

@app.route("/")
def home():
    return jsonify({"message": "Task API is running"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return jsonify([dict(task) for task in tasks])


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Task title is required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (data["title"], False)
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": new_id,
        "title": data["title"],
        "completed": False
    }), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    conn.close()
    return jsonify({"message": "Task deleted successfully"})

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    # Check if task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        conn.close()
        return jsonify({"error": "Task not found"}), 404

    # Update fields if provided
    title = data.get("title", task["title"])
    completed = data.get("completed", task["completed"])

    cursor.execute(
        "UPDATE tasks SET title = ?, completed = ? WHERE id = ?",
        (title, completed, task_id)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "id": task_id,
        "title": title,
        "completed": completed
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


@app.route("/")
def home():
    return jsonify({"message": "Task API is running"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    tasks = load_tasks()
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Task title is required"}), 400

    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": False
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify(new_task), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return jsonify({"message": "Task deleted"})

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:
            if "completed" in data:
                task["completed"] = data["completed"]
            if "title" in data:
                task["title"] = data["title"]

            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    for task in tasks:
        if task["id"] == task_id:
            if "completed" in data:
                task["completed"] = data["completed"]
            if "title" in data:
                task["title"] = data["title"]

            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
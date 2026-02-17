from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connect():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

#test route
@app.route('/')
def homepage():
    return '''<h1 style="font-family:Arial; color:green;">
    Server is up and running.</h1>
    <body style="background-color:black;"></body>'''

@app.get("/tasks")
def get_tasks():
    conn = db_connect()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(task) for task in tasks])

#creates tasks
@app.post("/addtask")
def create_task():
    data = request.get_json()

    #validates tasks
    if not data or "Task" not in data:
        return jsonify({"Error":"Title is required."}), 400

    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, done) VALUES (?, ?)",
        (data["Task"], data.get("Done", False))
        )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": task_id,
        "Task": data["Task"],
        "Done": data.get("Done", False)
    }), 201

#updates task
@app.put("/uptask/<int:id>")
def update_task(id):
    updated_task = request.get_json()

    #validates tasks
    if not updated_task or "Task" not in updated_task:
        return jsonify({"Error":"Invalid data"}), 400

    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET task = ?, done = ? WHERE id = ?",
        (updated_task["Task"], updated_task.get("Done", False), id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify(error = "Task not found"), 404

    conn.close()
    return jsonify(message = "Task updated successfully.")


#deletes tasks
@app.delete("/deltask/<int:id>")
def delete_task(id):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify(message = "Task not found."), 404

    conn.close()
    return jsonify(message = "Task deleted successfully.")
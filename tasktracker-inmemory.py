from flask import Flask, request, jsonify

app = Flask(__name__)

#in-memory database
tasks = []

#test route
@app.route('/')
def homepage():
    return '''<h1 style="font-family:Arial; color:green;">
    Server is up and running.</h1>
    <body style="background-color:black;"></body>'''

#creates tasks
@app.post("/tasks")
def create_task():
    data = request.get_json()

    #validates tasks
    if not data or "Task" not in data:
        return jsonify({"Error":"Title is required."}), 400

    if data["Task"] == "ShowAll":
        return jsonify(tasks)

    task = {
        "id": len(tasks) + 1,
        "Task": data["Task"],
        "Done": data.get("Done", False)
    }

    tasks.append(task)

    return jsonify(task), 201

#updates tasks
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    updated_task = request.get_json()

    #validates tasks
    if "Task" not in updated_task:
        return jsonify({"Error":"Invalid data"}), 400

    for task in tasks:
        if task["id"] == id:
            task["Task"] = updated_task["Task"]
            return jsonify(task)

    return jsonify(error="Task not found"), 404

#deletes tasks
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return jsonify(message="Task deleted successfully.")

    return jsonify(error="Task not found"), 404
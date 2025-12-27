from flask import Flask, request, jsonify, render_template
import models
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initialize database table
models.create_table()

# -----------------------
# Task Manager Routes
# -----------------------

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = models.get_tasks()
    task_list = []
    for task in tasks:
        label = "Completed" if task[4] else f"Priority {task[2]}"
        task_list.append({
            "id": task[0],
            "title": task[1],
            "priority": task[2],
            "due_date": task[3],
            "completed": bool(task[4]),
            "label": label
        })
    return jsonify(task_list)

# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    if not all(k in data for k in ("title", "priority", "due_date")):
        return jsonify({"error": "Missing data"}), 400

    models.add_task(data["title"], data["priority"], data["due_date"])
    return jsonify({"message": "Task created"}), 201

# Mark a task as completed
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def complete(task_id):
    models.complete_task(task_id)
    return jsonify({"message": "Task completed"})

# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    models.delete_task(task_id)
    return jsonify({"message": "Task removed"})

# -----------------------
# AI Route (New)
# -----------------------
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # Using the new ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Run Flask
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)

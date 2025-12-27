import sqlite3

def get_connection():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority INTEGER NOT NULL,
            due_date TEXT NOT NULL,
            completed INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Tasks table created or already exists")

def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY completed ASC, priority DESC, due_date ASC")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(title, priority, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, priority, due_date, completed) VALUES (?, ?, ?, 0)",
        (title, priority, due_date)
    )
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

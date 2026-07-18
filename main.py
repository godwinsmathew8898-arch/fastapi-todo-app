from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3

connection = sqlite3.connect("Task.db", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS lists(
        username VARCHAR(20),
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )
""")
connection.commit() # 

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/view/{userName}")
def viewTasks(userName: str):
    cursor = connection.cursor()
    data = cursor.execute("SELECT id, task FROM lists WHERE username=?", (userName,))
    tasks = data.fetchall()
    
    my_todos = []
    for task in tasks:
        my_todos.append({
            "id": task[0],
            "task": task[1]
        })
    return {"todo_list": my_todos}

@app.get("/add/{userName}/{new_task}")
def addTask(userName: str, new_task: str):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO lists(username, task) VALUES(?, ?)", (userName, new_task))
    connection.commit()
    return {"Message": "Success"}

@app.get("/delete/{task_id}")
def delete_task(task_id: int):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM lists WHERE id=?", (task_id,))
    connection.commit()
    return {"Deleted": "Deleted succesfully"}

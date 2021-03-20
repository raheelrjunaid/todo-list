# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

def listTodos(data):
    for count, todo in enumerate(data['todos'], 1):
        if todo['status'] == 'incomplete':
            print("[ ]", str(count) + ":", todo['title'])

def deleteTodo(todo_index):
    pass

clargs = argv[1:]
if "-n" in clargs:
    new_todo = input("Add a new todo: ")
    data = {
        "title": new_todo,
        "time": str(datetime.now()),
        "flag": True if "-f" in clargs else False,
        "status": "incomplete"
    }

    with open('data.json') as outfile:
        current_data = json.load(outfile)
        current_data['todos'].append(data)
        listTodos(current_data)

    with open('data.json', 'w') as outfile:
        json.dump(current_data, outfile, indent=2)

if clargs[0] == "-i":
    with open('data.json') as outfile:
        listTodos(json.load(outfile))
        action = input("Action: ")
        if action[0] == "d":
            if action[1].isdigit():
                pass
else:
    with open('data.json') as outfile:
        listTodos(json.load(outfile))

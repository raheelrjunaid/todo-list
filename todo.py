# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

json_file = 'data.json'
clargs = argv[1:]

def listTodos(data):
    for count, todo in enumerate(data['todos'], 1):
        if todo['status'] == 'incomplete':
            print("[ ]", str(count) + ":", todo['title'])

def deleteTodo(data, todo_index):
    data['todos'].pop(todo_index - 1)
    return data

if len(clargs) >= 1:
    if "-n" in clargs:
        new_todo = input("Add a new todo: ")
        data = {
            "title": new_todo,
            "time": str(datetime.now()),
            "flag": True if "-f" in clargs else False,
            "status": "incomplete"
        }

        with open(json_file) as outfile:
            current_data = json.load(outfile)
            current_data['todos'].append(data)
            listTodos(current_data)

        with open(json_file, 'w') as outfile:
            json.dump(current_data, outfile, indent=2)

    if clargs[0] == "-i":
        with open(json_file) as outfile:
            listTodos(json.load(outfile))
            action = input("Action: ")
            if action[0] == "d":
                if action[1].isdigit():
                    pass
    if clargs[0] == '-d':
        if clargs[1].isdigit:
            with open(json_file) as outfile:
                data = json.load(outfile)
            with open(json_file, 'w') as outfile:
                json.dump(deleteTodo(data, int(clargs[1])), outfile, indent=2)
else:
    with open(json_file) as outfile:
        listTodos(json.load(outfile))

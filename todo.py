# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

json_file = 'data.json'
clargs = argv[1:]

def listTodos(data):
    if len(data['todos']) == 0:
        print('No todos')
        return False
    for count, todo in enumerate(data['todos'], 1):
        status = "x" if todo['status'] == 'complete' else ' '
        print(f"[{status}]", str(count) + ":", todo['title'])

def deleteTodo(data, todo_index):
    data['todos'].pop(todo_index - 1)
    return data

with open(json_file) as outfile:
    read = json.load(outfile)

if len(clargs) >= 1:
    with open(json_file, 'w') as outfile:
        write = lambda data: json.dump(data, outfile, indent=2)
        if "-n" in clargs:
            new_todo = input("Add a new todo: ")
            new_todo = {
                "title": new_todo,
                "time": str(datetime.now()),
                "flag": True if "-f" in clargs else False,
                "status": "incomplete"
            }

            read['todos'].append(new_todo)
            listTodos(read)
            write(read)

        if clargs[0] == "-i":
            listTodos(read)
            action = input("Action: ")
            if action[0] == "d":
                if action[1].isdigit():
                    pass

        if clargs[0] == '-d':
            if clargs[1].isdigit():
                write(deleteTodo(read, int(clargs[1])))
        else:
            number = input("Which todo? ")
            write(deleteTodo(read, int(number)))

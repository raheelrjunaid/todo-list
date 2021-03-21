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
        status = "[x]" if todo['status'] == 'complete' else '[ ]'
        print(status, str(count) + ":", todo['title'])

def deleteTodo(todo_index):
    # TODO Change reliance on global var
    global read
    read['todos'].pop(todo_index - 1)

with open(json_file) as outfile:
    try:
        read = json.load(outfile)
    except json.decoder.JSONDecodeError:
        read = {
            "todos": []
        }

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

        if len(read['todos']) > 0:
            if clargs[0] == '-d':
                if len(clargs) >= 2 and clargs[1].isdigit():
                    try:
                        deleteTodo(int(clargs[1]))
                        listTodos(read)
                    except (IndexError, ValueError) as e:
                        print("Invalid option")
                else:
                    listTodos(read)
                    number = input("Which todo? ")
                    try:
                        deleteTodo(int(number))
                    except (IndexError, ValueError) as e:
                        print("Invalid option")
        else:
            print("Please add todo to proceed.")
        write(read)
else:
    listTodos(read)

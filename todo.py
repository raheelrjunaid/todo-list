# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

json_file = 'data.json' # The name of the json target file
clargs = argv[1:] # All command-line-args except file name

try:
    with open(json_file) as outfile:
        read = json.load(outfile)
# If the file doesn't exist or is empty: write file the default template
except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
    print("Error reading file: Creating base template (data.json)")
    with open(json_file, "w") as outfile:
        read = {"todos": []}
        json.dump(read, outfile, indent=2)

# TODO store read data in variable

def todosExist(todos=read['todos']) -> bool:
    if len(todos) == 0:
        print("No todos")
        return False
    else:
        return True

def sortTodos(data=read):
    todos = data['todos']
    def getGroups():
        groups = []
        for todo in todos:
            if todo['group'] not in groups:
                groups.append(todo['group'])
        return groups

    if todosExist(todos):
        sortedArray = []
        for group in getGroups():
            for todo in todos:
                if todo['group'] == group:
                    sortedArray.append(todo)
        data['todos'] = sortedArray
        return data

def listTodos(todos=read['todos']):
    if todosExist(todos):
        group = None
        for count, todo in enumerate(todos, 1):
            if todo['group'] != None and group != todo['group']:
                group = todo['group']
                print(group)
            # Set the checkbox based on todo status
            status = "[x]" if todo['status'] == 'complete' else '[ ]'
            if todo['flag']: # Print todo with flag icon if flagged
                print(status, str(count) + ":", todo['title'], '\uf024')
            else:
                print(status, str(count) + ":", todo['title'])

read = sortTodos()
# If the user supplies a command line argument, go into write mode
if len(clargs) >= 1:
    with open(json_file, 'w') as outfile:
        def numHandler(name):
            num = input(f"Which todo to {name}? ")
            if num.isdigit():
                return int(num)
            else:
                list_of_todos = []
                for char in num:
                    if char.isdigit():
                        list_of_todos.append(int(char))
                if list_of_todos:
                    return list_of_todos
                else:
                    raise ValueError

        # Change todo attributes
        def editTodo(action, todo_index):
            todo = read['todos'][todo_index - 1]
            if action == 'delete':
                todo['title'] = False
            elif action == "complete" or action == "incomplete":
                todo['status'] = action
            elif action == 'delete_all':
                read['todos'] = []
            elif action == 'edit':
                print("Editing todo:", todo_index)
                options = ['flag', 'title']
                for field_name in todo:
                    if field_name in options:
                        print(field_name + ":", todo[field_name])
                field = input("Field to change? ")
                if field == "flag":
                    todo['flag'] = False if todo['flag'] else True
                elif field == 'title':
                    todo['title'] = input("New title: ")
                else:
                    print('Not valid')
            return read

        def createTodo(title, group):
            new_todo = {
                "title": title,
                "date_created": str(datetime.now()),
                "flag": True if "-f" in clargs else False,
                "status": "incomplete",
                "group": group if group != '' else None
            }
            read['todos'].append(new_todo)
            return read

        try:
            write = lambda data: json.dump(data, outfile, indent=2)
            if "-n" in clargs:
                title = input("Add a new todo: ")
                group = input("Group (leave blank for none): ")
                read = sortTodos(createTodo(title, group))
                listTodos()
            options = {
                '-d': "delete",
                '-da': "delete_all",
                '-c': "complete",
                '-ic': "incomplete",
                '-e': "edit"
            }

            # Only execute if there are any todos and valid clargs
            if len(read['todos']) > 0 and clargs[0] in options:
                listTodos()
                # Word to be used in editTodo function
                word = options[clargs[0]]
                # Will either return and int or list
                todo_index = numHandler(word)
                if isinstance(todo_index, int): # One todo
                    read = editTodo(word, todo_index)
                else: # List of todos
                    for i in todo_index: # Iterate over action (word)
                        read = editTodo(word, i)
                    # Delete deactivated (title=False) todos
                    read['todos'] = [i for i in read['todos'] if i['title']]
                listTodos()

            elif clargs[0] in options:
                print("Please add todo to proceed.")

        # If user provides non-int or out of range int
        except (ValueError, IndexError) as e:
            print(e, "\nInvalid Option")
        except KeyboardInterrupt:
            print("\nExited Program, todos preserved")

        # Always write the modified data to the file
        finally:
            write(read)

# If there are no clargs, list all todos
else:
    listTodos()

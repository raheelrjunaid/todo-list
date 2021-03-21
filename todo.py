# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

json_file = 'data.json' # The name of the json target file
clargs = argv[1:] # All command-line-args except file name

def listTodos(data):
    if len(data['todos']) == 0:
        print('No todos')
    for count, todo in enumerate(data['todos'], 1):

        # Set the checkbox based on todo status
        status = "[x]" if todo['status'] == 'complete' else '[ ]'

        # Print name and number (for editing) of all todos
        if todo['flag']:
            print(status, str(count) + ":", todo['title'], '\uf024')
        else:
            print(status, str(count) + ":", todo['title'])

try:
    with open(json_file) as outfile:
        read = json.load(outfile)

# If the file doesn't exist or is empty
# Create/write to file the default template
except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
    print("Error reading file: Creating base template (data.json)")
    with open(json_file, "w") as outfile:
        read = {"todos": []}
        json.dump(read, outfile, indent=2)

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
            if action == "delete":
                read['todos'].pop(todo_index - 1)
            elif action == "complete" or action == "incomplete":
                todo['status'] = action
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

        # Catch any errors to prevent deletion of json_file contents
        try:
            write = lambda data: json.dump(data, outfile, indent=2)

            # TODO Add multiple todos
            # Create a new todo
            if "-n" in clargs:
                new_todo = input("Add a new todo: ")
                new_todo = {
                    "title": new_todo,
                    "date_created": str(datetime.now()),
                    "flag": True if "-f" in clargs else False,
                    "status": "incomplete"
                }

                read['todos'].append(new_todo)
                listTodos(read)

            # Only execute if there are any todos and valid clargs
            options = {
                '-d': "delete",
                '-c': "complete",
                '-ic': "incomplete",
                '-e': "edit"
            }

            if len(read['todos']) > 0 and clargs[0] in options:
                listTodos(read)
                word = options[clargs[0]]
                todo_index = numHandler(word)
                if isinstance(todo_index, int): # One todo
                    read = editTodo(word, todo_index)
                else: # List of todos
                    for i in todo_index:
                        read = editTodo(word, i)
                listTodos(read)
            elif clargs[0] in options:
                print("Please add todo to proceed.")

        # If user provides non-int or out of range int
        except (ValueError, IndexError) as e:
            print(e, "\nInvalid Option")
        except KeyboardInterrupt:
            print("\nExited Program, todos preserved")
        except Exception as e:
            print(e, "\nFailed")

        # Always write the modified data to the file
        finally:
            write(read)

# If there are no clargs, list all todos
else:
    listTodos(read)

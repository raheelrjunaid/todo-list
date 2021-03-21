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
        def editTodo(action, todo_index):
            todo = read['todos'][todo_index - 1]
            if action == "delete":
                read['todos'].pop(todo_index - 1)
            elif action == "complete" or action == "incomplete":
                todo['status'] = action
            elif action == 'edit':
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

            # Create a new todo
            if "-n" in clargs:
                new_todo = input("Add a new todo: ")
                new_todo = {
                    "title": new_todo,
                    "date_created": str(datetime.now()),
                    # TODO Add flag creation method
                    "flag": True if "-f" in clargs else False,
                    "status": "incomplete"
                }

                read['todos'].append(new_todo)
                listTodos(read)

            # Only execute if there are any todos and valid clargs
            options = ['-d', '-c', '-ic', '-e']
            if len(read['todos']) > 0 and clargs[0] in options:
                # TODO Delete & complete multiple todos
                listTodos(read)
                if clargs[0] == '-d': # Delete todo
                    number = int(input("Which todo to delete? "))
                    read = editTodo("delete", number)
                elif clargs[0] == '-c': # Complete todo
                    number = int(input("Which todo to complete? "))
                    read = editTodo("complete", number)
                elif clargs[0] == '-ic': # Incomplete todo
                    number = int(input("Which todo to incomplete? "))
                    read = editTodo("incomplete", number)
                elif clargs[0] == '-e': # Edit todo
                    number = int(input("Which todo to edit? "))
                    read = editTodo("edit", number)
                listTodos(read)
                # TODO Mark todo as complete and then delete
            else:
                print("Please add todo to proceed.")

        # If user provides non-int or out of range int
        except (ValueError, IndexError) as e:
            print(e, "Invalid Option")
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

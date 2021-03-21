# Todo list by Raheel Junaid: 03/20/21

from sys import argv
from datetime import datetime
import json

json_file = 'data.json' # The name of the json target file
clargs = argv[1:] # All command-line-args except file name

def listTodos(data):
    if len(data['todos']) == 0:
        print('No todos')
        return False
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
        json.dump({"todos": []}, outfile, indent=2)
        read = {"todos": []}

# If the user supplies a command line argument, go into write mode
if len(clargs) >= 1:
    with open(json_file, 'w') as outfile:
        deleteTodo = lambda todo_index: read['todos'].pop(todo_index - 1)

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

            # Only execute if there are any todos
            if len(read['todos']) > 0:
                # TODO Delete & complete multiple todos
                # Delete Todo
                if clargs[0] == '-d':
                    listTodos(read)
                    number = input("Which todo to delete? ")
                    deleteTodo(int(number))

                # Mark todo as complete
                elif clargs[0] == '-c':
                    listTodos(read)
                    number = input("Which todo to complete? ")
                # TODO Mark todo as complete and then delete
            else:
                print("Please add todo to proceed.")

        # If user provides non-int or out of range int
        except (ValueError, IndexError) as e:
            print(e, "Invalid Option")
        except KeyboardInterrupt:
            print("\nExited Program, todos preserved")

        # Any other exceptions
        except Exception:
            print(Exception, "\nFailed")

        # Always write the modified data to the file
        finally:
            write(read)

# If there are no clargs, list all todos
else:
    listTodos(read)

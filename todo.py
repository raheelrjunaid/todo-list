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

try:
    with open(json_file) as outfile:
        read = json.load(outfile)
            
except json.decoder.JSONDecodeError:
    read = {"todos": []}
    print("JSONError: File is empty, creating base template.")

except FileNotFoundError:
    print("data.json not found, creating file")
    with open(json_file, "w") as outfile:
        json.dump({"todos": []}, outfile, indent=2)
        read = {"todos": []}

if len(clargs) >= 1:
    with open(json_file, 'w') as outfile:
        try:
            write = lambda data: json.dump(data, outfile, indent=2)
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

            if len(read['todos']) > 0:
                # TODO Delete & complete multiple todos
                if clargs[0] == '-d':
                    listTodos(read)
                    number = input("Which todo to delete? ")
                    deleteTodo(int(number))
                elif clargs[0] == '-c':
                    listTodos(read)
                    number = input("Which todo to complete? ")
            else:
                print("Please add todo to proceed.")
        except (ValueError, IndexError) as e:
            print(e, "Invalid Option")
        except KeyboardInterrupt:
            print("\nExited Program, todos preserved")
        except Exception:
            print(Exception, "\nFailed")
        # finally:
        #     write(read)
else:
    listTodos(read)

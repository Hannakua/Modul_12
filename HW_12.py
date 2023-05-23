import sys
from classes import AddressBook, Record, Phone, Birthday, Iterable

filename = "users_contacts.txt"

USERS = AddressBook(filename)

def read_from_file():
    result = USERS.read_contacts_from_file()
    return result

USERS.data = read_from_file()
  
def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No such user"
        except ValueError:
            return 'Please, give me phone number(38XXX-XXX-XX or XXX-XXX-XX-XX) or birth in format dd/mm/yyyy.'
        except IndexError:
            return 'Enter user name'
        except TypeError:
            return "Phone: XXX-XXX-XX-XX, Date: dd/mm/yyyy"
    return inner


def hello():
    name = input('Hello, I am Bot. What is your name? ')
    return f'Hello, {name}! Can I help you?'

@error_handler
def unknown_command():
    
    return f"The command is wrong or empty. Please write command again or write help to see the possible command list."


def help():
    return "I am a bot. I accept the following commands: 'hello', 'add', 'change', 'show all', 'print pages', 'birth', 'exit', 'goodbye', 'close', 'save', 'search'. For 'add' or 'change' commands please enter the command in sequence: command user_name comma backspace user_number. For example: 'add Taras Kovalenko, 0676542345'"



@error_handler
def add_user(name, phone, birth = None):     # add user_name, phone_number, birthday(or not)

    if name not in USERS.data:
        user = Record(name, phone, birth)
    else:
        user = USERS[name]
        user.add_phone(phone)
        if birth is not None:
            user.add_birthday(birth)
    USERS.add_record(user)
    # USERS.write_contacts_to_file()
    result = user.user_record
    return result

def read_from_file():
    result = USERS.read_contacts_from_file()
    return result

@error_handler
def add_birth(name, birth, phone = None) :           # birth user_name, dd/mm/yyyy
    if name in USERS.data:
        user = USERS[name]
        user.add_birthday(birth)
    else:
        user = Record(name, phone, birth)
    USERS.add_record(user)
    return user.user_record

def days_to_birth(name):    # next birth user_name
    user = USERS[name]
    result = user.days_to_birthday()    
    return f"{result} days"

@error_handler
def change_phone(name, old_num, new_num):   # change user_name, old_number, new_number      
    user = USERS[name]     
    user.edit_phone(old_num, new_num)
    USERS.add_record(user)
    return user.user_record    

@error_handler
def phone_show(name):        #phone show user_name
    user = USERS[name]
    result = user.show_phones()
    return result

def show_all():  # show all
    if USERS == {}:
        result = "Not any record in phone book yet."
    else:
        USERS.show_all()

def show_part(n):  # print pages n
    iter = Iterable(int(n), USERS.data)
    for i in iter:
        print(i)

def write_to_file():                    # save
    USERS.write_contacts_to_file()

def search(search_str):                     # serch string
    result = USERS.search_data(search_str)
    return result
   
def exit():                 
    print('Good Bye!') 
    return sys.exit()

HANDLERS = {
    'help': help,
    'add': add_user,
    'show all': show_all,
    'exit': exit,
    'phone show': phone_show,
    'close': exit,
    'good bye': exit,
    'change': change_phone,  
    'birth': add_birth, 
    'print pages': show_part,
    'next birth': days_to_birth,
    'save': write_to_file,
    'search': search,
}

def identeficate_command(user_input):

    user_command, *data = user_input.strip().split(' ', 1)

    try:
        handler = HANDLERS[user_command.lower()]
        
    except KeyError:
        if data:
            command_part2, *data = data[0].strip().split(' ', 1)
            user_command = user_command + ' ' + command_part2       # якщо команда складається з двох слів через пробіл
        handler = HANDLERS.get(user_command.lower(), unknown_command)

    if data:
        data = data[0].split(',')
  
    return handler, data


def main():

    print(hello())

    while True:
        user_input = input('Please enter command: ')
    
        handler, data= identeficate_command(user_input)
   
        result = handler(*data)

        print(result)


if __name__ == "__main__":
    main()
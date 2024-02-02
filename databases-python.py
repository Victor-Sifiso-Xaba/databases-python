# Compulsory Task
#========Importing libraries==========
from tabulate import tabulate 
from colorama import Style
import sqlite3

#==========Dabase connect==================
'''Create database called ebookstore in directory'''
db = sqlite3.connect('ebookstore') 

cursor = db.cursor() #get a cursor object

#==========Functions==================
'''Create a function to print bold messages efficiently using colorama'''
def print_with_colorama(bold_message, message, style = Style.BRIGHT, style_reset = Style.RESET_ALL):
    print(style + f'\n{bold_message}: ' + style_reset + f'{message}\n')

'''Create a error handling function for numeric inputs using while loop'''
def get_numeric_input(prompt, data_type = int):
    while True:
        try:
            value = data_type(input(prompt))
            return value
        except ValueError:
            print_with_colorama('ValueError', f'Please enter a valid {data_type.__name__.lower()} value.')

'''Create a error handling function for white spaces using while loop'''
def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print_with_colorama('ValidationError', 'Please enter a non-empty value.')


'''Create a function to print the table from the ebookstore database'''
def get_table_print():
        # fetch all rows
        d = cursor.execute('''SELECT * FROM book
                    ''')
        rows = d.fetchall()

        # print the data using tabulate
        headers = ['id', 'title', 'author', 'qty']
        table = tabulate(rows, headers, tablefmt="fancy_grid")
        print(f'\nEbookstore data:\n {table}')

'''Create a function to create a table'''
def ebookstore_db():
    '''Check if the book table already exists'''
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='book'")
    table_exists = cursor.fetchone()

    '''if not exist, then create table a under try, else print error'''
    if not table_exists:
        # create a table called book in the database
        cursor.execute('''CREATE TABLE IF NOT EXISTS book(id INT PRIMARY KEY, title TEXT, author TEXT, qty INT)
                    ''')
        db.commit() # commit the changes

        #insert several books in the table
        books = [(3001,'A Tale of Two Cities','Charles Dickens',30),
                (3002,'Harry Potter and the Philosopher\'s Stone','J.K. Rowling',40),
                (3003,'The Lion, the Witch and the Wardrobe','C. S. Lewis',25),
                (3004,'The Lord of the Rings','J.R.R Tolkien',37),
                (3005,'Alice in Wonderland','Lewis Carroll',12),
                (3006,'Creativity Exaplained: From Music and Art to Innovation in Business','David Priilaid',2018)]

        try:
            cursor.executemany(
                ''' INSERT INTO book(id, title, author, qty) VALUES(?,?,?,?)
                ''', books)
            db.commit() # commit the changes

        except sqlite3.IntegrityError as e:
            print_with_colorama('DatabaseError', f'An error occurred: {e}')

        get_table_print() # print the table

    else:
        print_with_colorama('DatabaseError', 'The book table already exists in the database.')

        get_table_print() # print the table

'''Create a function to enter book in table'''
def enter_book():
    '''Print message that enter a book has been selected'''
    print_with_colorama('EnterBookSelected', 'you have selected to enter a book, details:')
    
    '''count the number of existing books to generate a new book id'''
    cursor.execute("SELECT COUNT(*) FROM book")
    book_count = cursor.fetchone()[0]
    new_book_id = 3000 + book_count + 1

    '''Prompt user to enter book data to store on database'''
    enter_book_title = get_non_empty_input('Enter the book title: ')
    enter_book_author = get_non_empty_input('\nEnter the book author: ')
    enter_book_quantity = get_numeric_input('\nEnter the book quantity: ')

    '''insert book data in the table'''
    enter_books = [(new_book_id,enter_book_title,enter_book_author,enter_book_quantity)]
    cursor.executemany(
        ''' INSERT INTO book(id, title, author, qty) VALUES(?,?,?,?)
        ''', enter_books)

    db.commit() # commit the changes

    get_table_print()  # print the table

    '''Print message that enter a book has been selected'''
    print_with_colorama('EnterBookCompleted', f'you have entered a book with id {new_book_id}')

    
def update_book():
    '''Print message that update a book has been selected'''
    print_with_colorama('UpdateBookSelected', 'you have selected to update a book, details:')
    
    '''Prompt user to enter book id to update on database'''
    update_book_id = str(input('Enter the book id: '))

    '''Create a menu to request user to perform actions'''
    update_book_menu = input('''\nSelect one of the following options:
    au - book author update
    qu - book quantity update
    tu - book title update
    0 - exit
    : ''').lower()

    if update_book_menu == 'au':
        # update a book's author
        update_book_author = get_non_empty_input('\nEnter the book author to update: ')
        cursor.execute('''UPDATE book SET author = ? WHERE id = ?
                    ''', (update_book_author, update_book_id))
       
        db.commit() # commit the changes     

        get_table_print()  # print the table

        '''Print message that update a book has been completed'''
        print_with_colorama('UpdateBookCompleted', f'you have updated author for id {update_book_id}')
        
    elif update_book_menu == 'qu':
        # update a book's quantity
        update_book_qty = get_numeric_input('\nEnter the book quantity to update: ')
        cursor.execute('''UPDATE book SET qty = ? WHERE id = ?
                    ''', (update_book_qty, update_book_id))
       
        db.commit() # commit the changes     

        get_table_print()  # print the table

    elif update_book_menu == 'tu':
        # update a book's title
        update_book_title = get_non_empty_input('\nEnter the book title to update: ')
        cursor.execute('''UPDATE book SET title = ? WHERE id = ?
                    ''', (update_book_title, update_book_id))
       
        db.commit() # commit the changes     

        get_table_print()  # print the table

        '''Print message that update a book has been completed'''
        print_with_colorama('UpdateBookCompleted', f'you have updated title for id {update_book_id}')

    elif update_book_menu == '0':
        '''Print message that exit has been selected'''
        print_with_colorama('Goodbye!!!', 'You have to re-run the program to open menu. :)')

        exit()

    else:
        print(Style.BRIGHT + "\nMenuOptionError: " + Style.RESET_ALL + "you have entered an invalid input. Please try again! :(\n")

def delete_book():
    '''Print message that delete a book has been selected'''
    print_with_colorama('DeleteBookSelected', 'you have selected to delete a book, details:')
    
    '''Prompt user to enter book data delete on database'''
    delete_book_id = int(input('Enter the book id to delete: '))

    # delete a book's row
    cursor.execute('''DELETE FROM book WHERE id = ?
            ''', (delete_book_id,))

    db.commit() # commit the changes     

    get_table_print()  # print the table

    '''Print message that update a book has been completed'''
    print_with_colorama('DeleteBookCompleted', f'you have deleted row for id {delete_book_id}')

def search_book():
    '''Print message that search a book has been selected'''
    print_with_colorama('SearchBookSelected', 'you have selected to search a book, details:')
    
    '''Prompt user to enter book data to store on database'''
    search_book_id = str(input('Enter the book id to search: '))

    d = cursor.execute('''SELECT id, title, author, qty FROM book WHERE id=?
                ''', (search_book_id,))

    db.commit() # commit the changes     

    # fetch all rows
    rows = d.fetchall()

    # print the data using tabulate
    headers = ['id', 'title', 'author', 'qty']
    table = tabulate(rows, headers, tablefmt="fancy_grid")
    print(f'\nEbookstore data after searching book from book table:\n {table}')

    '''Print message that update a book has been completed'''
    print_with_colorama('SearchBookCompleted', f'you have searched book id {search_book_id}')

#==========Menu==================
try:
    ebookstore_db()

    # Use a while True loop, show menu with various functions
    while True:

        menu = input('''Select one of the following options:
        1 - Enter book
        2 - Update book
        3 - Delete book
        4 - Search books
        0 - exit
        >>> ''').lower()


        if menu == '1':        
            # Call the function to enter a book
            enter_book()

        elif menu == '2':     
            # Call the function to update a book
            update_book()

        elif menu == '3':
            # Call the function to delete a book
            delete_book()
        
        elif menu == '4':
            # Call the function to search a book
            search_book()

        elif menu == '0':
            print(Style.BRIGHT + "\nGoodbye!!!" + Style.RESET_ALL + " You have to re-run the program to open menu. :)\n")
            db.close()
            exit()

        else:
            print(Style.BRIGHT + "\nMenuOptionError: " + Style.RESET_ALL + "you have entered an invalid input. Please try again! :(\n")

except sqlite3.Error as e:
    print_with_colorama('DatabaseError', f'An error occurred: {e}')      
    
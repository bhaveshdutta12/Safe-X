from tkinter import *
from tkinter import messagebox
import random
import pyperclip
from datetime import datetime
import mysql.connector

NAVY = '#000000'
GREY = '#bbbbbb'
BEIGE = '#ffe3d8'

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    numbers = list('0123456789')
    symbols = list('!@#$%^&*()_+')
    letters_lower = list(map(str.lower, letters))
    letters.extend(letters_lower)

    num_letters = random.randint(8, 10)
    num_numbers = random.randint(1, 2)
    num_symbols = random.randint(1, 2)

    rand_letters = [random.choice(letters) for i in range(num_letters)]
    rand_numbers = [random.choice(numbers) for i in range(num_numbers)]
    rand_symbols = [random.choice(symbols) for i in range(num_symbols)]

    created_password = rand_letters + rand_numbers + rand_symbols
    random.shuffle(created_password)
    created_password = ''.join(created_password)

    password_entry.delete(0, END)
    password_entry.insert(0, created_password)
    pyperclip.copy(created_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def saved_entries():
    user_website = website_entry.get()
    user_email = email_entry.get()
    user_password = password_entry.get()

    if len(user_website) != 0 and len(user_password) != 0:
        confirmation = messagebox.askyesno(title=user_website,
                                           message=f"\n'email': {user_email}\n'password': {user_password}\n\nPlease confirm before saving!")
        if confirmation:
            try:
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',
                    database='password_manager'
                )

                cursor = connection.cursor()

                query = "INSERT INTO passwords (website, email, password) VALUES (%s, %s, %s)"
                values = (user_website, user_email, user_password)
                cursor.execute(query, values)
                connection.commit()

                website_entry.delete(0, END)
                password_entry.delete(0, END)
                messagebox.showinfo(title='Success', message='Password saved successfully.')
            except mysql.connector.Error as error:
                messagebox.showerror(title='Error', message='Error saving password: ' + str(error))
            finally:
                cursor.close()
                connection.close()
        else:
            messagebox.showinfo(title='Canceled', message='Password not saved.')
    else:
        messagebox.showwarning(title='Oops', message="Please don't leave any fields empty!")

# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search_website():
    global website_entry
    user_website = website_entry.get().capitalize()

    try:
        connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='12345',
                database='password_manager'
        )

        cursor = connection.cursor()

        query = "SELECT password FROM passwords WHERE website = %s"
        values = (user_website,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            password_entry.delete(0, END)
            password_entry.insert(0, result[0])
        else:
            messagebox.showinfo(title='Not Found', message='Password not found for the given website.')
    except mysql.connector.Error as error:
        messagebox.showerror(title='Error', message='Error searching password: ' + str(error))
    finally:
        cursor.close()
        connection.close()

# ----------------



# ---------------------------- AUTHENTICATION PAGE ------------------------------- #

# ---------------------------- AUTHENTICATION PAGE ------------------------------- #

def authenticate():
    entered_password = password_entry.get()
    if entered_password == "test":
        # Password is correct, proceed to the password manager application
        auth_window.destroy()  # Close the authentication window
        open_password_manager()
    else:
        messagebox.showerror(title="Authentication Failed", message="Incorrect password. Please try again.")

def open_password_manager():
    global password_manager_window,website_entry,password_entry,email_entry
    # Create a new window for the password manager application
    password_manager_window = Tk()
    password_manager_window.title("Password Manager")
    password_manager_window.config(padx=50, pady=50)

    # ROW 0
    canvas = Canvas(height=200, width=200, bg=NAVY, highlightthickness=0)
    img = PhotoImage(file='logo.png')
    canvas.create_image(100, 100, image=img)
    canvas.grid(row=0, column=1)

    # ROW 1
    website_label = Label(text='Website:', bg=NAVY, fg=BEIGE)
    website_label.grid(row=1, column=0, sticky="W")

    website_entry = Entry(font=('Arial', 15))
    website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
    website_entry.focus()

    website_search = Button(text='Search', bg=GREY, command=search_website)
    website_search.grid(row=1, column=2, sticky="EW")

    # ROW 2
    email_label = Label(text='Email/Username:', bg=NAVY, fg=BEIGE)
    email_label.grid(row=2, column=0, sticky="W")

    email_entry = Entry(font=('Arial', 15))
    email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
    email_entry.insert(0, 'myusername@gmail.com')

    # ROW 3
    password_label = Label(text='Password:', bg=NAVY, fg=BEIGE)
    password_label.grid(row=3, column=0, sticky="W")

    password_entry = Entry(font=('Arial', 15))
    password_entry.grid(row=3, column=1, sticky="EW")

    password_button = Button(text='Generate Password', bg=GREY, command=random_password)
    password_button.grid(row=3, column=2, sticky="EW")

    # ROW 4
    button = Button(text='Add', bg=GREY, command=saved_entries)
    button.grid(row=4, column=1, columnspan=2, sticky="EW")
    button.config(pady=2)

    password_manager_window.mainloop()

# Create the authentication window
auth_window = Tk()
auth_window.title("Password Manager - Authentication")
auth_window.config(padx=50, pady=50)

# Create and position the authentication widgets
password_label = Label(auth_window, text="Enter Password:")
password_label.grid(row=0, column=0)

password_entry = Entry(auth_window, show="*")
password_entry.grid(row=0, column=1)

authenticate_button = Button(auth_window, text="Authenticate", command=authenticate)
authenticate_button.grid(row=1, column=0, columnspan=2)

auth_window.mainloop()

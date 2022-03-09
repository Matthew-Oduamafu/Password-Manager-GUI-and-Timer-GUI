import tkinter as tk
from tkinter import font
from tkinter.messagebox import askokcancel, showinfo
from password_generator import generate_password
import pyperclip
from time import sleep
import json

# path = E:\MATTHEW\MATTHEW\Passwords\
PATH = r"data.json"


# global functions for opening json files
def open_json_file(file_path, open_mode, new_data=None):
    if new_data is None:
        new_data = {}
    if open_mode == "r":
        with open(file_path, open_mode) as data_file:
            data = json.load(data_file)  # to save json data
        return data
    elif open_mode == "w":
        with open(file_path, open_mode) as data_file:
            json.dump(new_data, data_file, indent=4)  # to save json data
        return


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password_func():  # generates random secure password
    password_entry.delete(0, tk.END)
    password_entry.insert(tk.END, generate_password())


# -------------------- SEARCH FOR EXISTING WEBSITE & PASSWORD -------------------#
def search_website():
    website = website_entry.get().strip()
    if len(website) == 0:
        showinfo(title="Oops", message="Please enter website")
        return
    try:
        data = open_json_file(PATH, "r")
    except FileNotFoundError:
        showinfo(title="Error", message=f"No Data File Found")
        return
    except json.decoder.JSONDecodeError:
        showinfo(title="Error", message=f"No details for {website} exists")
        return
    else:
        if website in data.keys():
            user_info = data[website]
            pyperclip.copy(user_info['password'])
            showinfo(title=website, message=f"Email: {user_info['email']}\nPassword: {user_info['password']}")
        else:
            showinfo(title="Error", message=f"No details for {website} exists")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_user_info():
    email = email_or_username_entry.get().strip()
    website = website_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        showinfo(title="Oops", message="Please don't leave any field empty")
        return

    # confirm details entered
    answer = askokcancel(title=website, message=f"Details entered: \nEmail: {email} \nPassword: {password}")

    if answer:
        try:  # if json file exists then we update
            data = open_json_file(PATH, "r")
            data.update(new_data)
            open_json_file(PATH, "w", data)

        # if not then we create the file for the first time or if file is empty
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            open_json_file(PATH, "w", new_data)

        finally:
            pyperclip.copy(password)
            sleep(2 / 3)
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# adding canvas to window
logo_img = tk.PhotoImage(file="logo.png")  # logo to be added to canvas
canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# ~~~~~~~~~~~~~~~ adding all the labels ~~~~~~~~~~~~~~~~~~~#
# website label
website_label = tk.Label(text="Website:", font=("Times New Roman", 12, font.BOLD))
website_label.grid(row=1, column=0)

# email/username label
email_or_username_label = tk.Label(text="Email/Username:", font=("Times New Roman", 12, font.BOLD))
email_or_username_label.grid(row=2, column=0)

# password label
password_label = tk.Label(text="Password:", font=("Times New Roman", 12, font.BOLD))
password_label.grid(row=3, column=0)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ~~~~~~~~~~~~~~~ adding all the entry widgets ~~~~~~~~~~~#
widgets_width = 56
# website entry
website_entry = tk.Entry(width=36, font="consolas")
website_entry.grid(row=1, column=1)
website_entry.focus()

# email/username entry
email_or_username_entry = tk.Entry(width=widgets_width, font="consolas")
email_or_username_entry.grid(row=2, column=1, columnspan=2)
email_or_username_entry.insert(tk.END, "mattietorrent@gmail.com")

# password entry
password_entry = tk.Entry(width=36, font="consolas")
password_entry.grid(row=3, column=1)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ~~~~~~~~~~~~~~~ adding all the button widgets ~~~~~~~~~~~#
# generate password button
generate_password_button = tk.Button(text="Generate Password", width=24, font=("consolas", 10),
                                     command=generate_password_func)
generate_password_button.grid(row=3, column=2)

# add password button
add_info = tk.Button(text="Add", width=55, command=save_user_info, font="consolas")
add_info.grid(row=4, column=1, columnspan=2)

# add a search button
search_button = tk.Button(text="Search", width=24, font=("consolas", 10), command=search_website)
search_button.grid(row=1, column=2)

window.mainloop()

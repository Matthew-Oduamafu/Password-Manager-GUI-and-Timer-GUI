import tkinter as tk
from tkinter.messagebox import askyesno, showinfo
import pandas as pd
from random import choice
from time import sleep

BACKGROUND_COLOR = "#B1DDC6"
WAIT_TIME = 3000
current_card = {}
to_learn = {}

# read from csv file
try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
except pd.errors.EmptyDataError:
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
finally:
    if to_learn.__len__() == 0:
        to_learn = pd.read_csv("./data/french_words.csv").to_dict(orient="records")


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


def next_card():
    global to_learn
    global current_card, flip_timer

    if len(to_learn) == 0:
        yes_continue = askyesno(title="Completed",
                                message="Congrats!!\nYou've learnt all the words\nDo you want to start again?")
        if yes_continue:
            original_data_ = pd.read_csv("./data/french_words.csv")
            to_learn = original_data_.to_dict(orient="records")
        else:
            showinfo(title="Congratulations 🥳 🎉 🎊", message="Have a nice day😊😊")
            sleep(1)
            window.destroy()
            return
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(WAIT_TIME, func=flip_card)


# take learnt words out of the list
def is_known():
    to_learn.remove(current_card)
    data_to_save = pd.DataFrame(to_learn)
    data_to_save.to_csv("./data/words_to_learn.csv", index=False)
    next_card()
    pass


# ####################### Window ###################################
window = tk.Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(WAIT_TIME, func=flip_card)

# ######### Canvas for overlapping images and text ###################
card_back_img = tk.PhotoImage(file="./images/card_back.png")
card_front_img = tk.PhotoImage(file="./images/card_front.png")
canvas = tk.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("consolas", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("consolas", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# adding the image buttons
cross_image = tk.PhotoImage(file="./images/wrong.png")
unknown_button = tk.Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = tk.PhotoImage(file="./images/right.png")
known_button = tk.Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()  # to ensure tha we get our first french word

window.mainloop()

import tkinter as tk

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier New"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
checkmark = ""
res = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def restart_timer():
    global checkmark, res
    window.after_cancel(timer)
    checkmark = ""
    checkmark_label.config(text=checkmark)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    res = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
# function the start the time when the start button is clicked
def start_timer():
    global res
    res += 1
    # count_down(5*60)
    work_sec = 1 * 60  # WORK_MIN*60
    short_break_sec = 1 * 60  # SHORT_BREAK_MIN*60
    long_break_sec = 1 * 60  # LONG_BREAK_MIN*60
    if res % 8 == 0:
        timer_label.config(text="Long Break", fg=GREEN)
        count_down(long_break_sec)  # long break
    elif res % 2 == 1:
        timer_label.config(text="Work Time", fg=GREEN)
        count_down(work_sec)  # work time
    elif res % 2 == 0:
        timer_label.config(text="Short Break", fg=GREEN)
        count_down(short_break_sec)  # short break time


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global checkmark, timer
    m, s = divmod(count, 60)
    canvas.itemconfig(timer_text, text=f"{m:02d}:{s:02d}")
    if count >= 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        if res % 2 == 1:
            checkmark += "🗸"
            checkmark_label.config(text=checkmark)
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# create a canvas
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
canvas.grid(row=1, column=1)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))

# adding the labels
timer_label = tk.Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 38, "bold"))
timer_label.grid(row=0, column=1)

# checkmark label
checkmark_label = tk.Label(text=checkmark, bg=YELLOW, fg=GREEN, font=(FONT_NAME, 28, "bold"))
checkmark_label.grid(row=3, column=1)

# adding start & reset buttons
start_button = tk.Button(text="Start", bg=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)
reset_button = tk.Button(text="Reset", bg=YELLOW, highlightthickness=0, command=restart_timer)
reset_button.grid(row=2, column=2)

# Let the count down begin!!!!
# count_down(5)

window.mainloop()

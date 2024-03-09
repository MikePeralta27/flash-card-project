from tkinter import *
import pandas
from random import *

BACKGROUND_COLOR = "#B1DDC6"
french = "French"
english = "English"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(lang_label, text=french, fill="black")
    canvas.itemconfig(word_label, text=current_card[french], fill="black")
    canvas.itemconfig(bg_image, image=front_image)
    flip_timer = window.after(3000, func=flip_card)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfig(lang_label, text=english, fill="white")
    canvas.itemconfig(word_label, text=current_card[english], fill="white")
    canvas.itemconfig(bg_image, image=back_image)


# Create Window
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, func=flip_card)

# Create Canvas
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
bg_image = canvas.create_image(400, 263, image=front_image)
lang_label = canvas.create_text(400, 150, text=french, font=("Arial", 40, "italic"), fill="black")
word_label = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"), fill="black")
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
# Wrong button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

# Right button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()

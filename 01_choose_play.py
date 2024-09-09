from tkinter import *
from functools import partial  # To prevent unwanted windows


class ChooseRounds:

    def __init__(self):
        button_fg = "#FFFFFF"
        button_font = ("Arial", "13", "bold")

        # Initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # Set up GUI Frame
        self.intro_frame = Frame(padx=10, pady=10)
        self.intro_frame.grid()

        # Heading and introduction
        self.intro_heading_label = Label(self.intro_frame, text="Greek Gods",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        introduction = "Welcome to my quiz about Greek gods!" \
                       "To begin, click on 5, or 10 rounds," \
                       "or if you want to do a custom amount, click on custom!"
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=introduction,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1)

        # Rounds buttons...
        self.how_many_frame = Frame(self.intro_frame)
        self.how_many_frame.grid(row=2)

        self.output_label = Label(self.intro_frame, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=3)

        btn_colour_value = [
            ["#BE2727", 5], ["#276FBF", 10], ["#DFBA89", "Custom"]
        ]

        for item in range(0, 3):
            self.rounds_button = Button(self.how_many_frame,
                                        fg=button_fg,
                                        bg=btn_colour_value[item][0],
                                        text="{}".format(btn_colour_value[item][1]),
                                        font=button_font, width=10,
                                        command=lambda i=item: self.to_play(btn_colour_value[i][1])
                                        )
            self.rounds_button.grid(row=0, column=item,
                                    padx=5, pady=5)

    # print user selections
    def to_play(self, num_rounds):
        if num_rounds == "Custom":
            self.custom_rounds()
        else:
            print("You Chose {} rounds".format(num_rounds))

    # Custom rounds - When "Custom" is clicked, should open a second window
    def custom_rounds(self):
        self.custom_window = Toplevel(root)
        self.custom_window.title("Enter Number of Rounds")

        self.label = Label(self.custom_window, text="Enter a number (max 100):")
        self.label.grid(row=0, padx=10, pady=10)

        self.entry = Entry(self.custom_window)
        self.entry.grid(row=1, padx=10, pady=10)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.add_placeholder)

        # Output label for error messages
        self.output_label = Label(self.custom_window, text="",
                                  fg="#9C0000")
        self.output_label.grid(row=2, padx=10, pady=10)

        self.submit_button = Button(self.custom_window, text="Submit", command=self.submit_custom_rounds)
        self.submit_button.grid(row=3, padx=10, pady=10)

        self.placeholder = "Enter a number"
        self.placeholder_color = "grey"
        self.default_color = self.entry.cget("fg")
        self.add_placeholder(None)

    # clear the placeholder box automatically when an incorrect response is submitted
    def clear_placeholder(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, END)
            self.entry.config(fg=self.default_color, bg="white")

    def add_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg=self.placeholder_color)

    def submit_custom_rounds(self):
        has_error = "no"

        try:
            num_rounds = int(self.entry.get())
            if 1 <= num_rounds <= 100:
                print("You Chose {} rounds".format(num_rounds))
                self.custom_window.destroy()
            else:
                has_error = "yes"
                self.var_feedback.set("Please enter a number between 1 and 100.")
                self.output_label.config(fg="#9C0000")
                self.entry.config(bg="#F8CE00")
        except ValueError:
            has_error = "yes"
            self.var_feedback.set("ERROR - Please ensure you have entered a number.")
            self.output_label.config(fg="#9C0000")
            self.entry.config(bg="#F8CE00")

        if has_error == "yes":
            self.var_has_error.set("yes")
            self.output_label.config(text=self.var_feedback.get())
        else:
            self.var_has_error.set("no")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Greek Gods Quiz")
    ChooseRounds()
    root.mainloop()


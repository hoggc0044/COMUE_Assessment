from tkinter import *
import csv
import random


class Play:
    def __init__(self, csv_file):
        # Initialize the GUI
        self.root = Tk()
        self.root.title("The alleged gods")

        # Initialize tkinter variables after creating the root window
        self.correct_answer = StringVar()
        self.god_name = StringVar()

        self.data = self.load_csv_data(csv_file)
        self.score = 0
        self.current_question = None
        self.round_number = 1  # Track the round number
        self.total_rounds = len(self.data)  # Total number of rounds

        self.setup_gui()
        self.next_question()
        self.root.mainloop()

    def load_csv_data(self, file_path):
        data = []
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                god_info = {"God Name": row[2],
                            "Correct Answer": row[0]}  # Column C is the god's name, Column A is the correct answer
                data.append(god_info)
        return data

    def next_question(self):
        if len(self.data) > 0:
            self.current_question = random.choice(self.data)
            self.god_name.set(self.current_question['God Name'])
            self.correct_answer.set(self.current_question['Correct Answer'])
            self.data.remove(self.current_question)  # Remove the used question from the list
            self.update_round_label()
        else:
            self.question_label.config(text="Quiz Complete!")
            self.god_name.set("")
            self.button1.config(state=DISABLED)
            self.button2.config(state=DISABLED)
            self.button3.config(state=DISABLED)

    def check_answer(self, user_answer):
        if user_answer == self.correct_answer.get():
            self.score += 1
            self.score_label.config(text=f"Your Score: {self.score}")
        self.round_number += 1
        self.next_question()

    def show_help(self):
        help_message = "Click the correct button to identify whether the god is Greek or Roman."
        from tkinter import messagebox
        messagebox.showinfo("Help", help_message)

    def update_round_label(self):
        self.round_label.config(text=f"Round {self.round_number} of {self.total_rounds}")

    def setup_gui(self):
        # Title Label
        self.title_label = Label(self.root, text="The alleged gods", font=("Helvetica", 16, "bold"), bg="lightyellow")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        # Round Label
        self.round_label = Label(self.root, text=f"Round {self.round_number} of {self.total_rounds}",
                                 font=("Helvetica", 14))
        self.round_label.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        # Question Label
        self.question_label = Label(self.root, text="Is this god Greek or Roman?", font=("Helvetica", 14))
        self.question_label.grid(row=2, column=0, columnspan=3, pady=5)

        # God Name Label
        self.god_label = Label(self.root, textvariable=self.god_name, font=("Helvetica", 14))
        self.god_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Buttons for options
        self.button1 = Button(self.root, text="Option 1", font=("Helvetica", 12), bg="#1E90FF", fg="white",
                              command=lambda: self.check_answer("Greek"))
        self.button1.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.button2 = Button(self.root, text="Option 2", font=("Helvetica", 12), bg="#1E90FF", fg="white",
                              command=lambda: self.check_answer("Roman"))
        self.button2.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.button3 = Button(self.root, text="Option 3", font=("Helvetica", 12), bg="#1E90FF", fg="white",
                              command=lambda: self.check_answer("Other"))
        self.button3.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        # Score Label
        self.score_label = Label(self.root, text=f"Your Score: {self.score}", font=("Helvetica", 14))
        self.score_label.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Control Buttons
        self.play_summary_button = Button(self.root, text="PLAY SUMMARY", font=("Helvetica", 12, "bold"), bg="#BE2727",
                                          fg="white")
        self.play_summary_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.help_button = Button(self.root, text="HELP", font=("Helvetica", 12, "bold"), bg="#276FBF", fg="white",
                                  command=self.show_help)
        self.help_button.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.next_button = Button(self.root, text="NEXT", font=("Helvetica", 12, "bold"), bg="#DFBA89", fg="white",
                                  command=self.next_question)
        self.next_button.grid(row=6, column=2, padx=10, pady=5, sticky="ew")


# Instantiate and run the game
if __name__ == "__main__":
    quiz = Play('gods.csv')

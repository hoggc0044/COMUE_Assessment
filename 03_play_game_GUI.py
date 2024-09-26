from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


# While I test, I've set the number of rounds in to_play to 5, to simulate a user choosing 5 rounds.
# This should allow me to do adequate testing, and I can evaluate the end process when all rounds
# are completed.
class ChooseRounds:
    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_quiz(5)

    def to_quiz(self, num_rounds):
        Quiz(num_rounds)

        # Hide root window (ie: hide rounds option window).
        root.withdraw()


# The Play class handles the main gameplay.
class Quiz:
    def __init__(self, how_many):
        background = "#F6ECDB"
        # Initialize the user's score.
        self.user_score = 0
        # Create a new window for the quiz.
        self.play_box = Toplevel()

        # If users press cross at top, closes help
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_quiz))

        # Variables used to work out statistics, when game ends etc
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Initialize rounds played and rounds won; set to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # Load all data from the CSV file
        self.all_data = self.get_all_data()

        # Create the quiz frame.
        self.quiz_frame = Frame(self.play_box, width=300,
                                height=200, padx=10, pady=10,
                                bg=background)
        self.quiz_frame.grid()

        # Heading for the rounds.
        rounds_heading = f"Choose - Round 1 of {how_many}"
        self.choose_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Raleway", "16", "bold"),
                                    bg=background)
        self.choose_heading.grid(row=0)

        # Instructions for the quiz.
        instructions = "Choose one of the two options provided. " \
                       "You have a 50/50 chance of getting it right. " \
                       "When you're done, or if you get stuck, you can " \
                       "click on 'Help'."
        self.instructions_label = Label(self.quiz_frame, text=instructions,
                                        wraplength=350, justify="left",
                                        bg=background)
        self.instructions_label.grid(row=1, padx=5, pady=5)

        # Label for the current question.
        self.question_label = Label(self.quiz_frame, text="Is this god Greek or Roman?",
                                    wraplength=350, justify="center",
                                    font=("Helvetica", 16, "bold"), padx=5, pady=5,
                                    bg=background)
        self.question_label.grid(row=2)

        # Create the option buttons in a new frame.
        self.option_frame = Frame(self.quiz_frame)
        self.option_frame.grid(row=3)

        # Greek option button.
        self.option1_button = Button(self.option_frame, fg="#FFFFFF", width=17, bg="#276FBF",
                                     text="Greek", font=("Arial", "12", "bold"),
                                     command=lambda: self.check_answer("Greek"))
        self.option1_button.grid(row=0, column=0, padx=5, pady=5)

        # Roman option button.
        self.option2_button = Button(self.option_frame, fg="#FFFFFF", width=17, bg="#276FBF",
                                     text="Roman", font=("Arial", "12", "bold"),
                                     command=lambda: self.check_answer("Roman"))
        self.option2_button.grid(row=0, column=1)

        # Label for displaying the god's name.
        self.god_label = Label(self.quiz_frame, text="god name goes here",
                               bg="#F6ECDB", width=40, font=("Raleway", "12"))
        self.god_label.grid(row=4, padx=5, pady=5)

        # Label for displaying the user's choice and result.
        self.user_choice_label = Label(self.quiz_frame,
                                       text="When you choose an option,"
                                            "your choice will appear here!",
                                       bg="#DFBA89", width=52,)
        self.user_choice_label.grid(row=5, padx=5, pady=5)

        # Frame for round results and navigation.
        self.rounds_frame = Frame(self.quiz_frame)
        self.rounds_frame.grid(row=6, padx=5, pady=5)

        # Label for displaying the current round result.
        self.round_results_label = Label(self.rounds_frame, text="Your score and round info will appear here",
                                         width=44,
                                         font=("Arial", 10),
                                         bg=background)
        self.round_results_label.grid(row=0, column=0)

        # Control frame for navigation buttons.
        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=7)

        # Button to go to the next round.
        self.next_button = Button(self.control_frame, text="NEXT",
                                  fg="#FFFFFF", bg="#DFBA89",
                                  font=("Arial", 11, "bold"),
                                  width=19, state=DISABLED,
                                  padx=3, pady=3,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=2)

        # Button for help.
        self.help_button = Button(self.control_frame, text="HELP",
                                  fg="#FFFFFF", bg="#276FBF",
                                  font=("Arial", 11, "bold"),
                                  width=19,
                                  padx=3, pady=3,
                                  command=self.get_help)
        self.help_button.grid(row=0, column=1)

        # Start the first round.
        self.new_round()

    # Method to load data from the CSV file.
    def get_all_data(self):
        with open("00_quiz_info.csv", "r") as file:
            var_all_data = list(csv.reader(file, delimiter=","))
        # Remove the header row from the data.
        var_all_data.pop(0)
        return var_all_data

    # Method to start a new round.
    def new_round(self):
        # Disable the next button at the start of each round.
        self.next_button.config(state=DISABLED)
        self.option1_button.config(state=NORMAL)
        self.option2_button.config(state=NORMAL)

        # Check if the quiz is complete.
        if self.rounds_played.get() >= self.rounds_wanted.get():
            self.question_label.config(text="Quiz Complete!")
            self.option1_button.config(state=DISABLED)
            self.option2_button.config(state=DISABLED)
            self.user_choice_label.config(text=f"Your Score: {self.user_score} out of {self.rounds_wanted.get()}")
            return

        # Select a random question for the new round.
        current_question = random.choice(self.all_data)
        # Remove the selected question from the data.
        self.all_data.remove(current_question)

        # Set the question details.
        self.god_name = current_question[2]
        self.correct_answer = current_question[0]

        # Update the UI with the new question.
        self.god_label.config(text=self.god_name)
        self.choose_heading.config(text=f"Round {self.rounds_played.get() + 1} of {self.rounds_wanted.get()}")

    # Method to check the user's answer.
    def check_answer(self, user_answer):
        # Update the score if the answer is correct.
        if user_answer.lower() == self.correct_answer.lower():
            self.user_score += 1
            self.user_choice_label.config(text="Nicely done! \n"
                                               f"You've chosen the correct answer! \n"
                                               f"{self.god_name} is {self.correct_answer}.")
            self.round_results_label.config(
                text=f"Round {self.rounds_played.get() + 1}: Current score: {self.user_score}")

        else:
            self.user_choice_label.config(text="Uh oh! \n"
                                               "That answer doesn't look right!"
                                               f"{self.god_name} is {self.correct_answer}.")
            self.round_results_label.config(
                text=f"Round {self.rounds_played.get() + 1}: Current score: {self.user_score}")

        # Update the rounds played and enable the next button.
        self.rounds_played.set(self.rounds_played.get() + 1)
        self.next_button.config(state=NORMAL)
        self.option1_button.config(state=DISABLED)
        self.option2_button.config(state=DISABLED)

    # Static method for displaying help (placeholder).
    def get_help(self):
        DisplayHelp(self)

    # Method to close the quiz window.
    def close_quiz(self):
        root.destroy()


class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#F6ECDB"
        self.help_box = Toplevel()

        # disable help button
        partner.help_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=500,
                                height=400,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="HELP ME G",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Playing this quiz is quite simple." \
                    "Your task is to try and answer as many questions as you can correctly, \n" \
                    "and try to beat your previous scores. \n" \
                    "When running the game, you'll be given three round \n" \
                    "options - 5, 10 or a custom amount (1-100). \n" \
                    "Choose your rounds to start the quiz."

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#276FBF",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)


# closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...

        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# Main routine to start the program.
if __name__ == "__main__":
    root = Tk()
    root.title("Greek Gods Quiz")
    ChooseRounds()
    root.mainloop()


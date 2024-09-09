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
        self.to_play(5)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds option window).
        root.withdraw()


# The Play class handles the main gameplay.
class Play:
    def __init__(self, how_many):
        background = "#F6ECDB"
        # Initialize the user's score.
        self.user_score = 0
        # Create a new window for the quiz.
        self.play_box = Toplevel()

        # If users press cross at top, closes help
        self.play_box.protocol('WM_DELETE_WINDOW', partial(self.close_play))

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
                                       bg="#DFBA89", width=52, )
        self.user_choice_label.grid(row=4, padx=5, pady=5)

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
                                  width=12, state=DISABLED,
                                  padx=3, pady=3,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=3)

        control_buttons = [
            ["#BE2727", "SUMMARY", "Request Summary"],
            ["#276FBF", "HELP", "Receive Help"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 2):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        # Access stats and help buttons so that they can be
        # enabled and disabled
        self.summary_button = self.control_button_ref[0]
        self.help_button = self.control_button_ref[1]

        # disable stats button at start of game (as there
        # are no stats to display).
        self.summary_button.config(state=DISABLED)

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
            self.summary_button.config(state=NORMAL)
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

    def to_do(self, action):
        if action == "Receive Help":
            print("ERROR 404: Help unavailable")
        elif action == "Request Summary":
            DisplaySummary(self, self.user_score)

    @staticmethod
    def get_help():
        print("ERROR: 404 - Help not found")

    # Method to close the quiz window.
    def close_play(self):
        root.destroy()


class DisplaySummary:
    def __init__(self, partner, user_score):
        # setup dialogue box and background colour
        self.summary_box = Toplevel()

        summary_bg_colour = "#DAE8FC"

        # disable help button
        partner.summary_button.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.summary_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_summary, partner))

        self.summary_frame = Frame(self.summary_box, width=300,
                                 height=200, bg=summary_bg_colour)
        self.summary_frame.grid()

        self.help_heading_label = Label(self.summary_frame,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"),
                                        bg=summary_bg_colour)
        self.help_heading_label.grid(row=0)

        summary_text = "Here are your game statistics"
        self.help_text_label = Label(self.summary_frame, text=summary_text, wraplength=350,
                                     justify="left", bg=summary_bg_colour)
        self.help_text_label.grid(row=1, padx=10)

        # frame to hold statistics 'table'
        self.data_frame = Frame(self.summary_frame, bg=summary_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=2, padx=10, pady=10)

        # get statistics for user and computer
        self.user_summary = self.get_summary(user_score, "User")

        # background formatting for heading, odd and even rows
        head_back = "#FFFFFF"
        odd_rows = "#C9D6E8"
        even_rows = summary_bg_colour

        row_names = ["", "Total", "Best Score", "Worst Score", "Average Score"]
        row_formats = [head_back, odd_rows, even_rows, odd_rows, even_rows]

        # data for labels (one label / sub list)
        all_labels = []

        count = 0
        for item in range(0, len(self.user_summary)):
            all_labels.append([row_names[item], row_formats[count]])
            all_labels.append([self.user_summary[item], row_formats[count]])
            count += 1

        # create labels based on list above
        for item in range(0, len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0],
                                    bg=all_labels[item][1],
                                    width="10", height="2", padx=5
                                    )
            self.data_label.grid(row=item // 3,
                                 column=item % 3,
                                 padx=0, pady=0)

        # Dismiss button
        self.dismiss_button = Button(self.summary_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_summary,
                                                     partner))
        self.dismiss_button.grid(row=3, padx=10, pady=10)

    @staticmethod
    def get_summary(score_list, entity):
        total_score = sum(score_list)
        best_score = max(score_list)
        worst_score = min(score_list)
        average = total_score / len(score_list)

        return [entity, total_score, best_score, worst_score, average]

    # Method to close the quiz window.
    @staticmethod
    def close_summary(self):
        root.destroy()


# Main routine to start the program.
if __name__ == "__main__":
    root = Tk()
    root.title("Greek Gods Quiz")
    ChooseRounds()
    root.mainloop()

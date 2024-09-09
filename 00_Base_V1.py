from tkinter import *
from functools import partial # prevent unwanted windows
import csv
import random



class ChooseRounds:

    def __init__(self):
        # set play class to 5 rounds for testing
        self.to_play(5)

    # print user selections
    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root windows (ie: hide round choice window)
        root.withdraw()


class Play:

    def __init__(self, how_many):

        self.play_box = Toplevel()

        # If users press x at the top, close help
        # and release button
        self.play_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_play))

        # Varibles used to work out stats when game ends
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # Initially set rounds played and won to 0
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        # lists to hold user scores
        # used to work out stats

        user_scores = []

        # get all quest


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Greek Gods Quiz")
    ChooseRounds()
    root.mainloop()

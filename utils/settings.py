from tkinter import *
import tkinter as tk


class Settings(tk.Toplevel):
    """
    Encapsulates the methods required for drawing, initialized, creating, and handling the various settings menu
    and components.
    """

    def __init__(self, master):
        super().__init__()
        self.master = master

        self.title("Settings")
        self.colors = {"Black": 1,
                       "White": 2}
        self.modes = ["Human", "Computer"]
        self.configs = {"Standard": 1,
                        "German Daisy": 2,
                        "Belgian Daisy": 3
                        }
        self.color_choice = IntVar()
        self.mode_choice_p1 = StringVar()
        self.mode_choice_p2 = StringVar()
        self.board_config = IntVar()
        self.turn_value = IntVar()
        self.turn_value.set(20)
        self.turn_timer_value = IntVar()
        self.turn_timer_value.set(10)
        self.turn_timer_value2 = IntVar()
        self.turn_timer_value2.set(10)
        self.selections = {}
        self.font = "Montserrat", 10

    def main_window(self):
        """
        Calls helper methods to manage the settings window.
        """
        self.master.deiconify()
        self.destroy()

    def draw_settings(self):
        """
        Calls helper methods to draw the settings menu as well as its components.
        """
        self.player_color()
        self.game_mode()
        self.select_configuration()
        self.set_turn_limit()
        self.set_turn_timer()
        self.submit_button()

    def player_color(self):
        """
        Draws and creates the settings menu portion to allow the player to select which turn_color they would like
        to play as.
        """
        player_color_label = LabelFrame(self, text="Select Player 1 turn_color", font=self.font)
        player_color_label.grid(sticky=W, padx=10, pady=10)

        for (text, color) in self.colors.items():
            Radiobutton(player_color_label, text=text, variable=self.color_choice,
                        value=color, font=self.font, ).grid(sticky=W, column=1)

    def game_mode(self):
        """
        Draws and creates the settings menu portion allowing the player to select their desired game mode.
        """
        select_game_mode_label = LabelFrame(self, text="Select game mode", font=self.font)
        select_game_mode_label.grid(sticky=W, padx=10, pady=10)

        # for (text, mode) in self.modes.items():
        #     Radiobutton(select_game_mode_label, text=text, variable=self.mode_choice,
        #                 value=mode).grid(sticky=W)
        self.mode_choice_p1.set("Human")
        Label(select_game_mode_label, text="Player 1", font=self.font).grid(sticky=W)
        menu1 = OptionMenu(select_game_mode_label, self.mode_choice_p1, *self.modes)
        menu1.config(font=self.font)
        menu1.grid(sticky=W)
        self.mode_choice_p2.set("Computer")
        Label(select_game_mode_label, text="Player 2", font=self.font).grid(sticky=W)
        menu2 = OptionMenu(select_game_mode_label, self.mode_choice_p2, *self.modes)
        menu2.config(font=self.font)
        menu2.grid(sticky=W)

    def select_configuration(self):
        """
        Draws and creates the settings menu portion allowing the player to select their desired starting layout.
        """
        select_config_label = LabelFrame(self, text="Select starting configuration", font=self.font, )
        select_config_label.grid(sticky=W, padx=10, pady=10)

        for (text, config) in self.configs.items():
            Radiobutton(select_config_label, text=text, variable=self.board_config,
                        value=config, font=self.font).grid(sticky=W)

    def set_turn_limit(self):
        """
        Draws and creates the settings menu portion allowing the player to specify the maximum number of turns.
        """
        turn_limit_label = Label(self, text="Enter number of turns per player", font=self.font)
        turn_limit_label.grid()

        turns = Entry(self, textvariable=self.turn_value)
        turns.grid(pady=10)

    def set_turn_timer(self):
        """
        Draws and creates the settings menu portion allowing the player to specify the time limit for the player within
        the player 1 and 2 spot.
        """
        turn_time_limit_label = Label(self, text="Enter maximum time per turn\nPlayer 1", font=self.font)
        turn_time_limit_label.grid(padx=10)

        time = Entry(self, textvariable=self.turn_timer_value)
        time.grid(pady=10)

        turn_time_limit_label2 = Label(self, text="Enter maximum time per turn\nPlayer 2", font=self.font)
        turn_time_limit_label2.grid(padx=10)

        time2 = Entry(self, textvariable=self.turn_timer_value2)
        time2.grid(pady=10)

    def submit_button(self):
        """
        Draws, creates, and handles the submit button within the settings menu. Calls a helper method to retrieve the
        settings specified by the player.
        """
        submit = Button(self, text="Submit", command=self.get_data, font=self.font)
        submit.grid(pady=10)

    def get_data(self):
        """
        Retrieves the specified settings by the player and passes the settings to the main program loop.
        """
        self.selections['turn_color'] = self.color_choice.get()
        self.selections["mode_p1"] = self.mode_choice_p1.get()
        self.selections["mode_p2"] = self.mode_choice_p2.get()
        self.selections["config"] = self.board_config.get()
        self.selections["turns"] = self.turn_value.get()
        self.selections["time1"] = self.turn_timer_value.get()
        self.selections["time2"] = self.turn_timer_value2.get()
        self.main_window()

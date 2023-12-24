import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self, frame) -> None:
        '''Set up widgets for the dashboard frame.'''
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        # Create an instance of sql class.
        self.sql = SQL()
        self.create_window()

    def create_window(self):
        '''Create and place widgets within frame'''
        # Create cooridnate lists
        x = [33, 317]
        y = [50, 135, 220] # add 330 if a forth row is needed
        # Create label list for buttons and map them to the coorect function.
        labels = ['Load Anilox', 'Add Anilox', 'Delete Anilox',
                  'Set Parameters', 'Visual Apperance', 'Anilox Report']
        functions = [self.load_anilox, self.new_anilox, self.delete_anilox,
                     self.update_params, self.change_apperance, self.report]
        count = 0
        self.buttons = []
        for y_pos in y:
            for x_pos in x:
                new_btn = ttk.Button(
                    self.frame, text=labels[count], command=functions[count]
                )
                new_btn.place(x=x_pos, y=y_pos, width=250, height=50)
                count += 1
    
    def load_anilox(self) -> None:
        print('Load Anilox')

    def new_anilox(self) -> None:
        print('New Anilox')

    def delete_anilox(self) -> None:
        print('Delete anilox')

    def update_params(self) -> None:
        print('Update parameters')

    def change_apperance(self) -> None:
        print('Change look r')

    def report(self) -> None:
        print('Report')


class SQL:
    def __init__(self) -> None:
        pass
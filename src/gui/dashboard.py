import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, frame):
        '''Set up widgets for the dashboard frame.'''
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        # test label
        test_label = ttk.Label(self.frame, text='Dashboard').pack()
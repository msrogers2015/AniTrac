import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self) -> None:
        '''Creation of base software.'''
        # Create base GUI window
        self.root = tk.Tk()
        # Create size and location variables
        width = 600
        height = 400
        x = int((self.root.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.root.winfo_screenheight() / 2) - (height / 2))
        # Resize application window and center in screen
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        # Update application window title
        self.root.title('AniTrac')
        self.root.mainloop()


# Run application if this file is used as the main file
if __name__ == "__main__":
    # Create an instance of the applicaiton
    app = App()
import tkinter as tk
import os
import sqlite3
from tkinter import ttk, filedialog, messagebox

class Settings:
    def __init__(self, frame) -> None:
        '''Set up widgets for the dashboard frame.'''
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        # Create an instance of sql class.
        self.sql = SQL()
        self.create_window()

    def create_window(self) -> None:
        '''Create and place widgets within frame'''
        # Create cooridnate lists
        x = [33, 317]
        y = [50, 135, 220] # add 330 if a forth row is needed
        # Create label list for buttons and map them to the coorect function.
        labels = ['Load Anilox', 'Add Anilox', 'Delete Anilox',
                  'Set Parameters', 'Visual Apperance', 'Anilox Report']
        functions = [self.load_anilox, self.new_anilox, self.delete_anilox,
                     self.update_params, self.change_apperance, self.report]
        # Create a counter to select label and function from list
        count = 0
        # Create a list to place the buttons into. 
        self.buttons = []
        # Loop through the y coordinates
        for y_pos in y:
            # Loop through the x coorinate to create an x,y location pair
            for x_pos in x:
                # Create a new button with the label and fucntion from the list
                new_btn = ttk.Button(
                    self.frame, text=labels[count], command=functions[count]
                )
                # Place button based on the x,y coordinate pair
                new_btn.place(x=x_pos, y=y_pos, width=250, height=50)
                # Increase counter to progress through the lists.
                count += 1
                # Add button to the button list. 
                self.buttons.append(new_btn)
    
    def load_anilox(self) -> None:
        '''Load an entire list of anilox into database via CSV files.'''
        # Create a list of failed additions
        failures = {}
        # Create a list of acceptable file types to look for.
        file_types = (('CSV','*.csv'), ('All Files','*.*'))
        # Ask user to select file that contains the anilox list
        file = filedialog.askopenfile(filetypes=file_types)
        # If there is a valid selection, continue with this section of code.
        if file != None:
            # Open the csv file for parsing
            with open(file.name, 'r') as csv:
                # Loop through each line of the csv file
                for line in csv.readlines():
                    # Check to see if there is missing data in the record
                    if ('' in line.strip('\n').split(',') or
                        len(line.strip('\n').split(',')) != 3):
                        # If there is missing informaiton, add a failure
                        # message to teh record 
                        failures[roller] = 'Missing information'
                    else:
                        # Assign values variables to pass to the sql fucntion
                        # and clean the data
                        roller, lpi, bcm = line.strip('\n').split(',')
                        # Add record to the database
                        status = self.sql.add_anilox(roller, lpi, bcm)
                        # If value returned is true, continue to next record
                        if status:
                            continue
                        # If function returns an error code, add it to the
                        # failure list
                        else:
                            failures[roller] = status
        # If any records failed to be added to the database, alert the user of
        # the issue so proper action can be taken. 
        if len(failures) > 0:
            # Create a base message for the error message
            message = 'The following anilox rollers weren\'t added:\n'
            # Loop through failure dict and add failures to error message
            for key, value in failures.items():
                message += f'{key} - {value}\n'
            # Display a dialog box to user to alert them of failures.
            messagebox.showinfo(
                title='Failed Savings',
                message=message
            )

    def disable_buttons(self) -> None:
        '''Disable all buttons to prevent bugs.'''
        # Disable all buttons so other windows cannot be opened.
        for button in self.buttons:
            button.config(state='disable')

    def enable_buttons(self) -> None:
        '''Enable all buttons to return normal functionality.'''
        # Enable all buttons to resume normal functionality.
        for button in self.buttons:
            button.config(state='enable')

    def new_anilox(self) -> None:
        '''Add a new anilox to the list.'''
        # Disable all buttons so other windows cannot be opened.
        self.disable_buttons()
        self.toplevel = Anilox('New Anilox', self.enable_buttons)
        
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
        """Initialize class for database queries"""
        # Create a variable for the database
        self.db = os.path.join(os.getcwd(), "test.db")

    def connect(self) -> None:
        """Establish connection to database."""
        # Create connection to database
        self.con = sqlite3.connect(self.db)
        # Create cursor to naviagate and interact with the database
        self.cur = self.con.cursor()

    def disconnect(self) -> None:
        """Cleanly disconnect from the database."""
        # Close cursor to datbase
        self.cur.close()
        # Close connection to database
        self.con.close()

    def add_anilox(self, roller, lpi, bcm) -> str or bool:
        '''Add a new anilox to the database to track mileage.'''
        # Connect to database
        self.connect()
        # Create sql query to insert values into database
        sql = 'INSERT INTO anilox(roller, lpi, bcm) values(?,?,?)'
        try:
            # Try to insert record into database
            self.cur.execute(sql, (roller, lpi, bcm))
        # Catch any exeptions to display to end user and disconnect from the
        # database
        except Exception as e:
            self.disconnect()
            return str(e)
        # If there are no errors, save changes and close connection to database
        self.con.commit()
        self.disconnect()
        return True

class Anilox:
    def __init__(self, title, buttons) -> None:
        '''Create a top level window to interact with anilox.'''
        # Create window
        self.root = tk.Tk()
        # Create an instance of the sql class
        self.sql = SQL()
        # Update window title
        self.root.title(title)
        # Create a local function to enable buttons from the settings frame.
        self.enable_buttons = buttons
        # Create location variables
        x = int(self.root.winfo_screenwidth()/2 - 150)
        y = int(self.root.winfo_screenheight()/2 - 100)
        # Resize window
        self.root.geometry(f'300x200+{x}+{y}')
        # Update on close protocol so the setting buttons are also re-enabled.
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        # Set style
        self.set_style()
        # Create and place widets in the window
        self.create_window()

    def set_style(self) -> None:
        '''Update styling for the window.'''
        # Create a instance of the style class
        style = ttk.Style(self.root)
        # Change font size
        style.configure('.', font=(None, 14))

    def create_window(self) -> None:
        '''Create and place all widgets for the window'''
        # Create a list of items to be created
        widgets = ['Anilox','LPI','BCM']
        # List of size variables
        width = [75, 200, 150]
        height = 30
        # List of coordinates
        x = [10, 75]
        y = [10, 45, 80]
        self.entries = []
        # Loop through list to create labels and entries. Enumerate to get
        # numeric indices
        for index, value in enumerate(widgets):
            # Create and place the labels
            label = ttk.Label(self.root, text=value).place(
                x=x[0], y=y[index], width=width[0], height=height)
            # Create the entry box and increase the font size to 14 pt
            entry = ttk.Entry(self.root, font=(None, 14))
            # Place the entry box
            entry.place(x=x[1], y=y[index], width=width[1], height=height)
            # Add the entry to the list of entries.
            self.entries.append(entry)
        # Create button to add anilox to database
        add_btn = ttk.Button(
            self.root, text='Add Anilox',
            command=self.add_anilox)
        # Place add button widget
        add_btn.place(x=75, y=130, width=150, height=height)

    def add_anilox(self) -> None:
        '''Handler for adding anilox to records.'''
        # Create list of values from inforamtion in entry widtes
        data = [x.get() for x in self.entries]
        # If there is no blank spaces in data list, add record to database
        if '' not in data:
            # Create variables from the values in the entry widgets
            roller, lpi, bcm = data
            # Create a flag to control what happens after attempting to add
            # anilox to database
            flag = self.sql.add_anilox(roller, lpi, bcm)
            if flag:
                # If added succesfully, display confiramtion and close window.
                messagebox.showinfo(
                    title='Anilox Added.',
                    message=f'Anilox {self.entries[0].get()} successfully added.'
                )
                self.on_close()
        else:
            # Else, display error message and close window. 
            messagebox.showerror(
                title='Anilox Addition Failed',
                message='Failed to add anilox to the database.'
            )
            self.on_close()

    def on_close(self) -> None:
        '''Actions to be taken when the close button is pressed.'''
        try:
            # Try to enable buttons and destory window
            self.enable_buttons()
            self.root.destroy()
        except Exception:
            # In the event the application was closed first, continue to
            # Destory this window. 
            self.root.destroy()

class Delete:
    def __init__(self) -> None:
        pass
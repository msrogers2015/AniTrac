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
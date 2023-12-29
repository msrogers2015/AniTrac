import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


class Record:
    def __init__(self, frame, width) -> None:
        """Set up widgets for the dashboard frame."""
        # Assign class variable for frame to place widgets in
        self.frame = frame
        # Create an instance of the SQL class
        self.sql = SQL()
        # Create main window
        self.create_window(width)

    def set_style(self) -> None:
        """Set custom style for frame"""
        # Create style instance
        style = ttk.Style(self.frame)
        # Change font
        style.config(".", font=(None, 14))

    def create_window(self, width) -> None:
        """Create and add widgets to record anilox mileages"""
        # Create label and place
        mileage = ttk.Label(
            self.frame, text="Mileage", anchor="center", font=(None, 18)
        )
        mileage.place(x=(width - 150) / 2, y=25, width=150, height=30)
        # Create entry to record mileage and place widget
        self.mileage_entry = ttk.Entry(
            self.frame, font=(None, 14), justify="center"
        )
        self.mileage_entry.place(
            x=(width - 200) / 2, y=60, width=200, height=30
        )
        # Create a list to hold roller numbers
        self.rollers = []
        # Entry coordinates
        y_pos = [100, 145, 190, 230, 270]
        x_pos = [100, 350]
        # Create a list of rollers in the database
        rollers = [""] + self.sql.get_anilox_list()
        # Create a list to hold roller drop down widgets
        self.rollers = []
        # Create a list to hold drop down string variable widgets
        self.rollers_var = []
        # Counter to display the deck numbers
        count = 1
        # Loop through coordinate list to create a complete coordinate.
        for x in x_pos:
            for y in y_pos:
                # Offset to place unit string
                o = 75
                # Create string variable
                roller_var = tk.StringVar()
                # Create drop down widget and place in frame
                roller = ttk.OptionMenu(self.frame, roller_var, *rollers)
                roller.place(x=x, y=y, width=150, height=30)
                # Add string variable and drop down widget to their proper list
                self.rollers.append(roller)
                self.rollers_var.append(roller_var)
                # Create and place deck label.
                deck = ttk.Label(
                    self.frame, font=(None, 14), text=f"Deck {str(count)}"
                )
                deck.place(x=x - o, y=y, width=o, height=30)
                count += 1
        # Create button to increase mileage
        save_btn = ttk.Button(
            self.frame, text="Add Mileage", command=self.add_mileage
        )
        save_btn.place(x=(width - 150) / 2, y=315, width=150, height=40)

    def add_mileage(self) -> None:
        """Increase mileage for anilox rollers."""
        additional_mileage = self.mileage_entry.get().replace(',','')
        # If mileage is a whole number, continue with function
        if additional_mileage.isdigit():
            # Create a count variable to empty drop down menus.
            count = 0
            # Loop through rollers
            for roller in self.rollers_var:
                # If roller entry isn't empty, update mileage
                if roller.get() != "":
                    self.sql.add_mileage(
                        roller.get(), additional_mileage
                    )
                    # Reset drop down menu to be blank
                    roller.set("")
                    # Increase count to empty the correct drop down.
                    count += 1
            # Show confirmation
            messagebox.showinfo(
                title="Mileage Updated", message="Mileage has been updated"
            )
        else:
            # Show error message if mileage is incorrect.
            messagebox.showerror(
                title="Invalid Mileage",
                message="Please ensure a whole number is given for mileage.",
            )


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

    def get_anilox_list(self) -> list:
        """Get a list of all anilxo in the database."""
        # Connect to database
        self.connect()
        # Create sql statement to get all anilox information fromd database.
        sql = """SELECT roller FROM anilox"""
        # Execute query
        data = self.cur.execute(sql).fetchall()
        # Disconnect from database
        self.disconnect()
        # Create a list of the anilox after extracting them from the tuples.
        return [record[0] for record in data]

    def add_mileage(self, roller, mileage) -> None:
        """Increase mileage for anilox roller."""
        # Create new mileage after getting mileage from database and adding
        # new mileage from record window.
        new_mileage = self.get_mileage(roller) + int(mileage)
        # SQL statement
        sql = "UPDATE anilox SET mileage = ? where roller = ?"
        # Connect ot database
        self.connect()
        # Increase mileage
        self.cur.execute(sql, (new_mileage, roller))
        # Save changes
        self.con.commit()
        # Disconnect from database
        self.disconnect()

    def get_mileage(self, roller) -> int:
        """Get current mileage for anilox roller"""
        # Connect to database
        self.connect()
        # SQL Statement
        sql = """SELECT mileage FROM anilox where roller = ?"""
        # Get current mileage for anilox roller from database
        data = self.cur.execute(sql, (roller,)).fetchone()
        # Disconnect from database
        self.disconnect()
        # Return current mileage for anilox roller as an integer.
        return int(data[0])

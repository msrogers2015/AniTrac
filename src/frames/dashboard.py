from tkinter import ttk
import os
import json
import sqlite3


class Dashboard:
    def __init__(self, frame, width) -> None:
        """Set up widgets for the dashboard frame."""
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        # Create instance of sql class
        self.sql = SQL()
        # Load variables from config file
        self.load_json()
        self.create_table(width)
        self.style_table()

    def load_json(self) -> None:
        """Create variables based on the config file."""
        # Open config.json to convert json to dict
        with open("config.json", "r") as file:
            # Read the file and dump the json as a dict under the variable
            # data
            data = json.loads(file.read())
            # Create a limit variable to hi-lite roller over or near cleaning
            # limit
            self.limit = data["max_milage"]

    def style_table(self) -> None:
        """Create custom style for table"""
        # Color pallet
        green = "#79B43C"
        gray = "#C2C2C2"
        blue = "#289CCD"
        red = "#e4002b"
        yellow = "#fce300"
        # Create instance of style object
        style = ttk.Style(self.frame)
        # Create style map
        # Update table heading font size
        style.configure("Treeview.Heading", font=(None, 18))
        style.map(
            "Treeview",
            background=[("selected", green)],
            foreground=[("!selected", "black")],
        )
        # Create alternating row colors
        self.table.tag_configure("even", background=gray)
        self.table.tag_configure("odd", background="white")
        # Create color coding to create visual aid for anilox rollers nearing
        # limit or are already above limit.
        self.table.tag_configure("over_limit", background=red)
        self.table.tag_configure("near_limit", background=yellow)

    def create_table(self, width) -> None:
        """Create tree view widget to act as a table for displaying
        information"""
        # Create table widget. Show headings enable the columns to be displayed
        # at the top of the table providing headings.
        self.table = ttk.Treeview(self.frame)
        # Create scroll bar to navigate through all records and configure it
        # To the table
        self.yscroll = ttk.Scrollbar(self.frame, orient="vertical")
        self.yscroll.configure(command=self.table.yview)
        self.table.config(
            yscrollcommand=self.yscroll.set, selectmode="extended"
        )
        # Define columns
        self.table["columns"] = ("Anilox", "LPI", "BCM", "Feet")
        # Set a column width to evenly space all records.
        col_width = int((width - 20) / 5)
        # Create phantom column
        self.table.column("#0", width=50, minwidth=50)
        self.table.heading("#0", text="PID")
        # Loop through the columns to create the columns and insert the
        # headings
        for col in self.table["columns"]:
            # When creating the column, adjust the width, the mininum allowed
            # width and center the text in the header
            self.table.column(
                col, anchor="center", width=col_width, minwidth=col_width
            )
            # Assign the column the proper header and center the text.
            self.table.heading(col, text=col, anchor="center")
        # Display headings
        self.table["show"] = "headings"
        # Place the table in the frame with a padding of 10 on the top, left
        # and right side while leaving room at the bottom.
        self.table.place(x=10, y=10, width=width - 40, height=300)
        self.yscroll.place(x=width - 30, y=10, width=20, height=300)

    def populate_table(self) -> None:
        """Insert anilox records into table"""
        # Get anilox records
        records = self.sql.get_data()
        # Create a counter to alternate record background colros
        count = 0
        # Loop through records in database
        for record in records:
            # Check if record is above the specified limit
            if record[3] > self.limit:
                self.table.insert(
                    parent="",
                    index="end",
                    iid=count,
                    values=record,
                    tags=("over_limit",),
                )
            # If record isn't above the limit, check if the record is over 80%
            # towards the limit.
            elif record[3] > (self.limit * 0.8):
                self.table.insert(
                    parent="",
                    index="end",
                    iid=count,
                    values=record,
                    tags=("near_limit",),
                )
            # If the record is less than 80% towards the limti and the count is
            # even, set the row color to the even tag
            elif count % 2 == 0:
                self.table.insert(
                    parent="", index="end", iid=count, values=record,
                    tags=("even",)
                )
            # Else, set the odd rows color to the odd tag.
            else:
                self.table.insert(
                    parent="", index="end", iid=count, values=record,
                    tags=("odd",)
                )
            # Increase count by one to prevent iid from having two records with
            # the same id as well as keep the alternating pattern going.
            count += 1

    def update_table(self) -> None:
        """Clear records from table and insert updated information"""
        # Delete all records from the table
        for record in self.table.get_children():
            self.table.delete(record)
        # Populate the table with up to date information via grabbing it
        # directly from the datbase before inserting it into the table.
        self.populate_table()


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

    def get_data(self) -> list:
        """Gather all anilox information from database"""
        # Create sql statement.
        sql = """SELECT * FROM anilox"""
        # Connect to database
        self.connect()
        # Grab all anilox records from the database
        data = self.cur.execute(sql).fetchall()
        # Disconnect from the database
        self.disconnect()
        # Return data list for the parent function to use.
        return data

import tkinter as tk
import os
import json
import sqlite3
from datetime import date
from tkinter import ttk, filedialog, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox


class Settings:
    def __init__(self, frame) -> None:
        """Set up widgets for the dashboard frame."""
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        # Create an instance of sql class.
        self.sql = SQL()
        self.create_window()

    def create_window(self) -> None:
        """Create and place widgets within frame"""
        # Create cooridnate lists
        x = [33, 317]
        y = [50, 135, 220]  # add 330 if a forth row is needed
        # Create label list for buttons and map them to the coorect function.
        labels = [
            "Load Anilox",
            "Add Anilox",
            "Delete Anilox",
            "Set Parameters",
            "Load Database",
            "Export Database",
        ]
        functions = [
            self.load_anilox,
            self.new_anilox,
            self.delete_anilox,
            self.update_params,
            self.import_data,
            self.export_data,
        ]
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
        """Load an entire list of anilox into database via CSV files."""
        # Create a list of failed additions
        failures = {}
        # Create a list of acceptable file types to look for.
        file_types = (("CSV", "*.csv"), ("All Files", "*.*"))
        # Ask user to select file that contains the anilox list
        file = filedialog.askopenfile(filetypes=file_types)
        # If there is a valid selection, continue with this section of code.
        if file is not None:
            # Open the csv file for parsing
            with open(file.name, "r") as csv:
                # Loop through each line of the csv file
                for line in csv.readlines():
                    # Check to see if there is missing data in the record
                    if (
                        "" in line.strip("\n").split(",")
                        or len(line.strip("\n").split(",")) != 3
                    ):
                        roller = line.strip('\n').split(',')[0]
                        # If there is missing informaiton, add a failure
                        # message to teh record
                        failures[roller] = "Missing information"
                    else:
                        # Assign values variables to pass to the sql fucntion
                        # and clean the data
                        roller, lpi, bcm = line.strip("\n").split(",")
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
            message = "The following anilox rollers weren't added:\n"
            # Loop through failure dict and add failures to error message
            for key, value in failures.items():
                message += f"{key} - {value}\n"
            # Display a dialog box to user to alert them of failures.
            messagebox.showinfo(title="Failed Savings", message=message)

    def disable_buttons(self) -> None:
        """Disable all buttons to prevent bugs."""
        # Disable all buttons so other windows cannot be opened.
        for button in self.buttons:
            button.config(state="disable")

    def enable_buttons(self) -> None:
        """Enable all buttons to return normal functionality."""
        # Enable all buttons to resume normal functionality.
        for button in self.buttons:
            button.config(state="enable")

    def new_anilox(self) -> None:
        """Add a new anilox to the list."""
        # Disable all buttons so other windows cannot be opened.
        self.disable_buttons()
        # Create window to add new anilox
        self.toplevel = Anilox(self.enable_buttons)

    def delete_anilox(self) -> None:
        """Remove anilox from database."""
        # Disable all buttons so the other windows cannot be opened.
        self.disable_buttons()
        # Create window to remove anilox from database
        self.toplevel = Delete(self.enable_buttons)

    def update_params(self) -> None:
        """Change system defaults based on end user need."""
        # Disable all buttons so the other windows cannot be opened.
        self.disable_buttons()
        # Create window to update application configurations.
        self.toplevel = Parameters(self.enable_buttons)

    def import_data(self) -> None:
        """Load database with information."""
        Data("Import")

    def export_data(self) -> None:
        """Export information from database"""
        Data("Export")


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

    def add_anilox(self, roller, lpi, bcm, mileage=0) -> str or bool:
        """Add a new anilox to the database to track mileage."""
        # Connect to database
        self.connect()
        # Create sql query to insert values into database
        if mileage != 0:
            sql = """
                INSERT INTO anilox(roller, lpi, bcm, mileage) values(?,?,?,?)
            """
        else:
            sql = "INSERT INTO anilox(roller, lpi, bcm) values(?,?,?)"
        try:
            # Try to insert record into database
            if mileage != 0:
                self.cur.execute(sql, (roller, lpi, bcm, mileage))
            else:
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

    def delete_anilox(self, roller) -> bool:
        """Remove anilox from database"""
        # Connect to database
        self.connect()
        # SQL query to remove anilox roller from database.
        sql = """DELETE FROM anilox WHERE roller = ?"""
        try:
            # Remove anilox from database
            self.cur.execute(sql, (roller,))
            self.con.commit()
        except Exception as e:
            # Catch and display exception
            print(e)
            return False
        return True

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

    def dump_data(self) -> list:
        """Dump data from database."""
        # Connect to database
        self.connect()
        # SQL statement
        sql = "SELECT * FROM anilox"
        data = self.cur.execute(sql).fetchall()
        return [record for record in data]


class Anilox:
    def __init__(self, buttons) -> None:
        """Create a top level window to add new anilox to database."""
        # Create window
        self.root = tk.Tk()
        # Create an instance of the sql class
        self.sql = SQL()
        # Update window title
        self.root.title("New Anilox")
        # Create a local function to enable buttons from the settings frame.
        self.enable_buttons = buttons
        # Create location variables
        x = int(self.root.winfo_screenwidth() / 2 - 150)
        y = int(self.root.winfo_screenheight() / 2 - 100)
        # Resize window
        self.root.geometry(f"300x200+{x}+{y}")
        # Update on close protocol so the setting buttons are also re-enabled.
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Set style
        self.set_style()
        # Create and place widets in the window
        self.create_window()
        # Force focus on widnow
        self.root.focus_force()

    def set_style(self) -> None:
        """Update styling for the window."""
        # Create a instance of the style class
        style = ttk.Style(self.root)
        # Change font size
        style.configure(".", font=(None, 14))

    def create_window(self) -> None:
        """Create and place all widgets for the window"""
        # Create a list of items to be created
        widgets = ["Anilox", "LPI", "BCM"]
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
            label = ttk.Label(self.root, text=value)
            label.place(
                x=x[0], y=y[index], width=width[0], height=height
            )
            # Create the entry box and increase the font size to 14 pt
            entry = ttk.Entry(self.root, font=(None, 14))
            # Place the entry box
            entry.place(x=x[1], y=y[index], width=width[1], height=height)
            # Add the entry to the list of entries.
            self.entries.append(entry)
        # Create button to add anilox to database
        add_btn = ttk.Button(
            self.root, text="Add Anilox", command=self.add_anilox
        )
        # Place add button widget
        add_btn.place(x=75, y=130, width=150, height=height)

    def add_anilox(self) -> None:
        """Handler for adding anilox to records."""
        # Create list of values from inforamtion in entry widtes
        data = [x.get() for x in self.entries]
        # If there is no blank spaces in data list, add record to database
        if "" not in data:
            # Create variables from the values in the entry widgets
            roller, lpi, bcm = data
            # Create a flag to control what happens after attempting to add
            # anilox to database
            flag = self.sql.add_anilox(roller, lpi, bcm)
            if flag:
                # If added succesfully, display confiramtion and close window.
                roller = self.entries[0].get()
                messagebox.showinfo(
                    title="Anilox Added.",
                    message=f"Anilox {roller} successfully added.",
                )
                self.on_close()
        else:
            # Else, display error message and close window.
            messagebox.showerror(
                title="Anilox Addition Failed",
                message="Failed to add anilox to the database.",
            )
            self.on_close()

    def on_close(self) -> None:
        """Actions to be taken when the close button is pressed."""
        try:
            # Try to enable buttons and destory window
            self.enable_buttons()
            self.root.destroy()
        except Exception:
            # In the event the application was closed first, continue to
            # Destory this window.
            self.root.destroy()


class Delete:
    def __init__(self, buttons) -> None:
        """Create a top level window to remove anilox from database."""
        # Create windwo
        self.root = tk.Tk()
        # Create an instance of the sql class
        self.sql = SQL()
        # Update window title
        self.root.title("Delete Anilox")
        # Cteate a local function to enable buttons from the settings frame.
        self.enable_buttons = buttons
        # Create location variables
        x = int(self.root.winfo_screenwidth() / 2 - 150)
        y = int(self.root.winfo_screenheight() / 2 - 60)
        # Resize window
        self.root.geometry(f"300x120+{x}+{y}")
        # Update on close protocol so the setting buttons are also re-enabled.
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Set style
        self.set_style()
        # Create and place widgets in window
        self.create_window()
        # Force focus on window
        self.root.focus_force()

    def set_style(self) -> None:
        """Update styling for the window."""
        # Create a instance of the style class
        style = ttk.Style(self.root)
        # Change font size
        style.configure(".", font=(None, 14))

    def create_window(self) -> None:
        """Create and place all widgets for the window."""
        # Create and place label
        anilox = ttk.Label(self.root, text="Select Anilox")
        anilox.place(
            x=10, y=10, width=125, heigh=30
        )
        # Create drop down list for anilox selection
        self.anilox_list = AutocompleteCombobox(
            self.root, font=(None, 14),
            completevalues=[""] + self.sql.get_anilox_list()
        )
        # Change font of items in drop down menu
        self.anilox_list.place(x=135, y=10, width=150, height=30)
        # Create delete button
        self.delete_btn = ttk.Button(
            self.root, text="Delete", command=self.delete_anilox
        )
        self.delete_btn.place(x=75, y=50, width=150, height=40)

    def delete_anilox(self) -> None:
        """Delete an anilox from the database"""
        # Check if the entered anilox is part of the list
        if self.anilox_list.get() in self.sql.get_anilox_list():
            if self.sql.delete_anilox(self.anilox_list.get()):
                messagebox.showinfo(
                    title="Anilox Removed",
                    message=f"{self.anilox_list.get()} successfully deleted.",
                )
                self.on_close()
            else:
                messagebox.showerror(
                    title="Error Removing Anilox",
                    message=f"Error removing {self.anilox_list.get()}.",
                )
                self.on_close()
        else:
            messagebox.showwarning(
                title="Incorrect Information",
                message=f"{self.anilox_list.get()} couldn't be found.",
            )
            self.on_close()

    def on_close(self) -> None:
        """Actions to be taken when the close button is pressed."""
        try:
            # Try to enable buttons and destory window
            self.enable_buttons()
            self.root.destroy()
        except Exception:
            # In the event the application was closed first, continue to
            # Destory this window.
            self.root.destroy()


class Parameters:
    def __init__(self, buttons) -> None:
        """Create a top level window to remove anilox from database."""
        # Create windwo
        self.root = tk.Tk()
        # Create an instance of the sql class
        self.sql = SQL()
        # Update window title
        self.root.title("Update Parameters")
        # Cteate a local function to enable buttons from the settings frame.
        self.enable_buttons = buttons
        # Create location variables
        x = int(self.root.winfo_screenwidth() / 2 - 150)
        y = int(self.root.winfo_screenheight() / 2 - 60)
        # Resize window
        self.root.geometry(f"300x120+{x}+{y}")
        # Update on close protocol so the setting buttons are also re-enabled.
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # Set style
        self.set_style()
        # Create and place widgets in window
        self.create_window()
        # Load current configurations
        self.get_current_parameters()
        # Force focus on window
        self.root.focus_force()

    def get_current_parameters(self) -> list:
        """Get the current parameters in the config file"""
        # Open config.json and cache values
        with open("config.json", "r") as file:
            data = json.loads(file.read())
            mileage = data["max_mileage"]
            uom = data["uom"]
        return [mileage, uom]

    def create_window(self) -> None:
        """Create and place all widgets for the window."""
        # Get config information
        data = self.get_current_parameters()
        # Create and place labels
        uom = ttk.Label(self.root, text="UOM")
        uom.place(x=10, y=10, width=125, height=30)
        mileage_limit = ttk.Label(self.root, text="Cleaning Limit")
        mileage_limit.place(x=10, y=45, width=125, height=30)
        # Create list of acceptable unit of measuremetns
        self.uom_list = ["", "Feet", "Meters"]
        # Create a variable for unit of measurements
        self.uom_var = tk.StringVar(self.root)
        # Update variable based on data from config json.
        if data[1] == "Feet":
            self.uom_var.set(self.uom_list[1])
        elif data[1] == "Meters":
            self.uom_var.set(self.uom_list[2])
        # Create uom drop down and mileage limit entry
        self.uom = ttk.OptionMenu(self.root, self.uom_var, *self.uom_list)
        self.mileage = ttk.Entry(self.root, font=(None, 14))
        # Place widgets
        self.uom.place(x=145, y=10, width=145, height=30)
        self.mileage.place(x=145, y=45, width=145, height=30)
        # Create and place button
        save_btn = ttk.Button(
            self.root, text="Update", command=self.save_parameters
        )
        save_btn.place(x=75, y=75, width=150, height=40)

    def set_style(self) -> None:
        """Update styling for the window."""
        # Create a instance of the style class
        style = ttk.Style(self.root)
        # Change font size
        style.configure(".", font=(None, 14))

    def save_parameters(self) -> None:
        """Update parameters in configureation json file."""
        # Create local variables from input widgets while stripping
        # the placement seperators from mileage
        mileage = self.mileage.get().replace(",", "")
        uom = self.uom_var.get()
        # Create a blank variable to save dict from json
        data = None
        # Check if mileage is numeric and if uom is in the given list
        if mileage.isdigit() and uom in self.uom_list:
            # Open and copy config information as a local dict
            with open("config.json", "r") as file:
                data = json.loads(file.read())
                # Update dict with current configurations
                data["max_mileage"] = int(mileage)
                data["uom"] = uom
            # Open config file and clear it out to insert new information
            with open("config.json", "w") as file:
                file.write(str(json.dumps(data)))
            # Display confirmation.
            messagebox.showinfo(
                title="Configurations Updated",
                message="Configuration values have been updated.",
            )
            # Close window after saving values.
            self.on_close()
        else:
            # Display error message if updating configuration values fail.
            messagebox.showerror(
                title="Error Saving Configurations",
                message="There were issues updating the configurations.",
            )
            self.on_close()

    def on_close(self) -> None:
        """Actions to be taken when the close button is pressed."""
        try:
            # Try to enable buttons and destory window
            self.enable_buttons()
            self.root.destroy()
        except Exception:
            # In the event the application was closed first, continue to
            # Destory this window.
            self.root.destroy()


class Data:
    def __init__(self, report_type) -> None:
        """
        Save information from database or import information into database.
        """
        # Create an instance of the sql class
        self.sql = SQL()
        # Specify report type.
        self.report = report_type
        self.select_file()

    def select_file(self) -> None:
        """Select file to import or create export file."""
        # Create date variable for file name
        date_stamp = str(date.today())
        # Update title for file dialog
        title = f"{self.report} Data"
        # Create a list of acceptable file types to look for.
        file_types = (("CSV", "*.csv"), ("All Files", "*.*"))
        # Create dialog box based on if data is being imported or exported.
        if self.report == "Import":
            file = filedialog.askopenfile(filetypes=file_types, title=title)
        else:
            file = filedialog.asksaveasfile(
                filetypes=file_types,
                defaultextension=".csv",
                initialfile=f"anitrac_{date_stamp}",
                title=title,
            )
        # If dialog box has a valid path, continue to import or export data.
        if file is not None:
            if self.report == "Import":
                self.import_data(file.name)
            else:
                self.export_data(file.name)

    def export_data(self, path) -> None:
        """
        Save database information for user to import in case of corruption
        or updates
        """
        # Grab data from database
        data = self.sql.dump_data()
        # Open file to dump data
        with open(path, "w") as file:
            file.write("Roller, LPI, BCM, Mileage\n")
            for record in data:
                roller, lpi, bcm, mileage = record
                file.write(f"{roller},{lpi},{bcm},{mileage}\n")

    def import_data(self, path) -> None:
        """Import data into database from output file."""
        # Create a list variable
        failures = []
        # Open file and insert records into list
        with open(path, "r") as file:
            # Loop through records in database file
            for record in file.readlines()[1:]:
                # Split records into four variables and pass information to
                # add anilox function
                roller, lpi, bcm, mileage = record.split(",")
                status = self.sql.add_anilox(roller, lpi, bcm, mileage)
                # If function returns true, continue to next record
                if status:
                    continue
                else:
                    # Add any failures to list to display to end user
                    failures.append(roller)
        # If there are any failures, display an error message and list
        # all failures
        if len(failures) > 0:
            # Build the error message adn seperate anilox rollers with a comma
            message = "There was an issue adding the following rollers:\n\n"
            for roller in failures:
                message += f"{roller}, "
            # Display error message
            messagebox.showerror(title="Error Adding Rollers", message=message)
        else:
            # Display confirmation message.
            messagebox.showinfo(
                title="Data Successfully Loaded",
                message="Anilox successfully added to database.",
            )

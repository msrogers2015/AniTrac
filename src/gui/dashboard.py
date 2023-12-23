from tkinter import ttk
import os

class Dashboard:
    def __init__(self, frame, width) -> None:
        '''Set up widgets for the dashboard frame.'''
        # Assign class variable for frame to place widgets in.
        self.frame = frame
        self.create_table(width)
        self.style_table()
        self.sql = SQL()

    def style_table(self) -> None:
        '''Create custom style for table'''
        # Color pallet
        green = '#79B43C'
        gray = '#C2C2C2'
        blue = '#289CCD'
        # Create instance of style object
        style = ttk.Style(self.frame)
        # Create style map
        # Update table heading font size
        style.configure('Treeview.Heading', font=(None, 18))
        style.map("Treeview",
                  background = [('selected',green)],
                  foreground=[('!selected','black')]
        )
        # Create alternating row colors
        self.table.tag_configure('even', background='white')
        self.table.tag_configure('odd', background=gray)

    def create_table(self, width) -> None:
        '''Create tree view widget to act as a table for displaying
        information'''
        # Create table widget. Show headings enable the columns to be displayed
        # at the top of the table providing headings. 
        self.table = ttk.Treeview(self.frame)
        # Create scroll bar to navigate through all records and configure it
        # To the table
        self.yscroll = ttk.Scrollbar(self.frame, orient='vertical')
        self.yscroll.configure(command=self.table.yview)
        self.table.config(
            yscrollcommand= self.yscroll.set, selectmode='extended'
        )
        # Define columns
        self.table['columns'] = ('Anilox','LPI','BCM','Feet')
        # Set a column width to evenly space all records.
        col_width = int((width-20)/5)
        #Create phantom column
        self.table.column("#0", width=50, minwidth=50)
        self.table.heading("#0", text="PID")
        # Loop through the columns to create the columns and insert the
        # headings
        for col in self.table['columns']:
            # When creating the column, adjust the width, the mininum allowed
            # width and center the text in the header
            self.table.column(
                col, anchor='center', width=col_width, minwidth=col_width
            )
            # Assign the column the proper header and center the text. 
            self.table.heading(col, text=col, anchor='center')
        # Display headings
        self.table["show"] = "headings"
        # Place the table in the frame with a padding of 10 on the top, left
        # and right side while leaving room at the bottom. 
        self.table.place(x=10, y=10, width = width - 40, height=300)
        self.yscroll.place(x=width-30, y=10, width = 20, height=300)

    def populate_table(self) -> None:
        pass
        '''for x in range(5):
            if x % 2 == 0:
                self.table.insert(parent='', index='end', iid=x, values=record, tags=('even',))
            else:
                self.table.insert(parent='', index='end', iid=x, values=record, tags=('odd',))
                '''

    def update_table(self) -> None:
        '''Clear records from table and insert updated information'''
        for record in self.table.get_children():
            self.table.delete(record)

class SQL:
    def __init__(self) -> None:
        '''Initialize class for database queries'''
        # Create a variable for the database
        self.db = os.path.join(os.getcwd(), 'anitrac.db')
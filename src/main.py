import tkinter as tk
from tkinter import ttk
from frames import dashboard, settings, record

class App:
    def __init__(self) -> None:
        '''Creation of base software.'''
        # Create base GUI window
        self.root = tk.Tk()
        # Create size and location variables
        self.width = 600
        height = 400
        x = int((self.root.winfo_screenwidth() / 2) - (self.width / 2))
        y = int((self.root.winfo_screenheight() / 2) - (height / 2))
        # Resize application window and center in screen
        self.root.geometry(f'{self.width}x{height}+{x}+{y}')
        self.root.resizable(0,0)
        # Update application window title
        self.root.title('AniTrac')
        # Set style
        self.create_style()
        # Adjust padding for tabs to make them more visually appealing. 
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.create_tabs()
        self.root.mainloop()
    
    def create_style(self) -> None:
        '''Change style of tkinter notebook'''
        # Create style for notebook
        self.style = ttk.Style(self.root)
        # Color pallet
        self.green = "#79B43C"
        self.gray = "#C2C2C2"
        self.blue = "#289CCD"
        self.red = "#e4002b"
        self.yellow = "#fce300"
        self.style.configure('.', font=(None, 14))
        self.style.configure("TNotebook.Tab", padding=(55,0))

    def create_tabs(self) -> None:
        '''Create application windows and place in base application.'''
        # Create and pack notebook for tabs in application root
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(expand=1, fill='both')
        # Create frames to hold widgets for each tab.
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.record_frame = ttk.Frame(self.notebook)
        settings_frame = ttk.Frame(self.notebook)
        # Create local instances for gui
        self.dashboard_gui = dashboard.Dashboard(self.dashboard_frame, self.width)
        self.record_gui = record.Record(self.record_frame)
        self.settings_gui = settings.Settings(settings_frame)
        # Create tabs to navigate the different sub-windows
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        self.notebook.add(self.record_frame, text='Record')
        self.notebook.add(settings_frame, text='Settings')
        # Bind tab changing event to various functionalities. 
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event) -> None:
        '''Actions to be taken when tab change event happens.'''
        # If the index of the tab is one, update the table data in the
        # dashboard
        if self.notebook.index(self.notebook.select()) == 0:
            self.dashboard_gui.update_table()
    
    def on_close(self) -> None:
        '''Ensure all sub-windows are closed upon exiting the application'''
        try:
            # Try to close any active toplevel windows
            self.settings_gui.toplevel.on_close()
            self.root.destroy()
        except Exception as e:
            # If no toplevel windows exist, exit application.
            self.root.destroy()

# Run application if this file is used as the main file
if __name__ == "__main__":
    # Create an instance of the applicaiton
    app = App()
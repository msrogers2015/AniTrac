import tkinter as tk
from tkinter import ttk
from gui import dashboard, settings, record

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
        # Create a style for the application to customize gui
        style = ttk.Style(self.root)
        # Increase font size
        style.configure('.', font=(None, 14))
        # Adjust padding for tabs to make them more visually appealing. 
        style.configure('TNotebook.Tab', padding=(20,0))
        self.create_tabs()
        self.root.mainloop()

    def create_tabs(self) -> None:
        '''Create application windows and place in base application.'''
        # Create and pack notebook for tabs in application root
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')
        # Create frames to hold widgets for each tab.
        dashboard_frame = ttk.Frame(self.notebook)
        record_frame = ttk.Frame(self.notebook)
        settings_frame = ttk.Frame(self.notebook)
        # Create local instances for gui
        dashboard_gui = dashboard.Dashboard(dashboard_frame)
        record_gui = record.Record(record_frame)
        settings_gui = settings.Settings(settings_frame)
        # Create tabs to navigate the different sub-windows
        self.notebook.add(dashboard_frame, text='Dashboard')
        self.notebook.add(record_frame, text='Record')
        self.notebook.add(settings_frame, text='Settings')
        
    def bindings(self):
        pass


# Run application if this file is used as the main file
if __name__ == "__main__":
    # Create an instance of the applicaiton
    app = App()
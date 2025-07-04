import tkinter as tk
from database import initialize_connection
from ui.welcome_screen import WelcomeWindow

mydb, cursor = initialize_connection()

root = tk.Tk()
root.configure(bg="#d8c4ba")
root.resizable(False, False)
WelcomeWindow(root, mydb, cursor)
root.mainloop()
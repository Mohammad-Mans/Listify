import tkinter as tk
from tkinter import messagebox
from database import login
from .home_screen import HomeWindow
from .shared import center_window

class LoginWindow(tk.Frame):
    def __init__(self, master, mydb, cursor):
        super().__init__(master, bg="#d8c4ba")
        self.cursor = cursor
        self.mydb = mydb
        self.master.title("Login")
        center_window(master, 400, 400)

        tk.Label(self, text="Login", font=("Arial", 24, "bold"), bg="#d8c4ba").pack(pady=20)
        tk.Label(self, text="Username:", bg="#d8c4ba").pack(pady=5)
        self.username_entry = tk.Entry(self, width=40)
        self.username_entry.pack()

        tk.Label(self, text="Password:", bg="#d8c4ba").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", width=40)
        self.password_entry.pack()

        tk.Button(self, text="Login", bg="#c5a491", width=20, height=2, command=self.login_user).pack(pady=20)
        tk.Button(self, text="Go Back", bg="gray", width=10, command=self.on_back).pack()
        self.pack(fill='both', expand=True)

    def login_user(self):
        data = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get()
        }

        if not data["username"] or not data["password"]:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        if login(self.cursor, data):
            self.destroy()
            HomeWindow(self.master, self.mydb, self.cursor)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def on_back(self):
        from .welcome_screen import WelcomeWindow 
        self.destroy()
        WelcomeWindow(self.master, None, self.cursor)


import tkinter as tk
from .login_screen import LoginWindow
from .signup_screen import RegisterWindow
from .shared import center_window

class WelcomeWindow(tk.Frame):
    def __init__(self, master, mydb, cursor):
        super().__init__(master, bg="#d8c4ba")
        self.master.title("Listify")
        self.mydb = mydb
        self.cursor = cursor
        center_window(master, 400, 700)

        tk.Label(self, text="Listify", font=("Arial", 36, "bold"), bg="#d8c4ba").pack(pady=80)
        tk.Button(self, text="Login", font=("Arial", 16), bg="black", fg="white", width=20, height=2, command=self.on_login).pack(pady=20)
        tk.Button(self, text="Signup", font=("Arial", 16), bg="black", fg="white", width=20, height=2, command=self.on_register).pack(pady=20)
        self.pack(fill='both', expand=True)

    def on_login(self):
        self.destroy()
        LoginWindow(self.master,self.mydb, self.cursor)

    def on_register(self):
        self.destroy()
        RegisterWindow(self.master, self.mydb, self.cursor)

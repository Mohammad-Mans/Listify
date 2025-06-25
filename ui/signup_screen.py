import tkinter as tk
from tkinter import messagebox
from database import register
from .shared import center_window

class RegisterWindow(tk.Frame):
    def __init__(self, master, mydb, cursor):
        super().__init__(master, bg="#d8c4ba")
        self.master.title("Signup")
        self.mydb = mydb
        self.cursor = cursor
        center_window(master, 400, 600)

        tk.Label(self, text="Signup", font=("Arial", 24, "bold"), bg="#d8c4ba").pack(pady=20)

        tk.Label(self, text="Username:", bg="#d8c4ba").pack(pady=5)
        self.username = tk.Entry(self, width=40)
        self.username.pack()

        tk.Label(self, text="Store Name:", bg="#d8c4ba").pack(pady=5)
        self.store_name = tk.Entry(self, width=40)
        self.store_name.pack()

        tk.Label(self, text="Phone:", bg="#d8c4ba").pack(pady=5)
        self.phone = tk.Entry(self, width=40)
        self.phone.pack()

        tk.Label(self, text="Password:", bg="#d8c4ba").pack(pady=5)
        self.password = tk.Entry(self, width=40, show="*")
        self.password.pack()

        tk.Label(self, text="Password again:", bg="#d8c4ba").pack(pady=5)
        self.confirm_password = tk.Entry(self, width=40, show="*")
        self.confirm_password.pack()

        tk.Button(self, text="Signup", bg="#c5a491", width=20, height=2, command=self.register_user).pack(pady=20)
        tk.Button(self, text="Go Back", bg="gray", width=10, command=self.on_back).pack()

        self.pack(fill='both', expand=True)

    def register_user(self):
        username = self.username.get()
        storeName = self.store_name.get()
        phone = self.phone.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if username and storeName and phone and password:
            data = {
                "username": username,
                "store_name": storeName,
                "phone": phone,
                "password": password
            }
            register(self.mydb, self.cursor, data)
            messagebox.showinfo("Success", "User registered successfully!")
            self.destroy()
            from .welcome_screen import WelcomeWindow
            WelcomeWindow(self.master, self.mydb, self.cursor)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def on_back(self):
        from .welcome_screen import WelcomeWindow
        self.destroy()
        WelcomeWindow(self.master, self.mydb, self.cursor)

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

        self.create_field("Username:", "username")
        self.create_field("Store Name:", "store_name")
        self.create_field("Phone:", "phone")
        self.create_field("Password:", "password", show="*")
        self.create_field("Password again:", "confirm_password", show="*")

        tk.Button(self, text="Signup", bg="#c5a491", width=20, height=2, command=self.register_user).pack(pady=20)
        tk.Button(self, text="Go Back", bg="gray", width=10, command=self.on_back).pack()
        self.pack(fill='both', expand=True)

    def create_field(self, label_text, attr_name, show=None):
        tk.Label(self, text=label_text, bg="#d8c4ba").pack(pady=5)
        entry = tk.Entry(self, width=40, show=show) if show else tk.Entry(self, width=40)
        entry.pack()
        setattr(self, f"{attr_name}_entry", entry)

    def register_user(self):
        username = self.username_entry.get()
        storeName = storeName = self.store_name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

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

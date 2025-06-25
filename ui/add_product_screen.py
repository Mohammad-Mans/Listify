import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from database import add_product
from .shared import center_window
from .home_screen import HomeWindow  

class AddProductWindow(tk.Frame):
    def __init__(self, master, mydb, cursor):
        super().__init__(master, bg="#d8c4ba")
        self.master = master
        self.mydb = mydb
        self.cursor = cursor
        self.master.title("Add New Product")
        center_window(master, 400, 600)

        tk.Label(self, text="Add Product", font=("Arial", 18, "bold"), bg="#d8c4ba").pack(pady=20)

        tk.Label(self, text="Product Name:", bg="#d8c4ba").pack()
        self.name = tk.Entry(self, width=30)
        self.name.pack()

        tk.Label(self, text="Price:", bg="#d8c4ba").pack()
        self.price = tk.Entry(self, width=30)
        self.price.pack()

        tk.Label(self, text="Quantity:", bg="#d8c4ba").pack()
        self.quantity = tk.Entry(self, width=30)
        self.quantity.pack()

        tk.Label(self, text="Product Image:", bg="#d8c4ba").pack(pady=(10, 0))
        self.image = tk.Entry(self, width=30)
        self.image.pack()

        self.img_label = tk.Label(self, bg="#d8c4ba")
        self.img_label.pack(pady=10)

        tk.Button(self, text="Choose Image from Device", command=self.choose_image, width=25).pack()

        tk.Button(self, text="Save Product", bg="#4caf50", fg="white", width=20, height=2, command=self.save_product).pack(pady=15)
        tk.Button(self, text="Back", bg="#c5a491", width=20, height=2, command=self.go_back).pack()

        self.pack(fill='both', expand=True)

    def choose_image(self):
        filepath = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if filepath:
            self.image.delete(0, tk.END)
            self.image.insert(0, filepath)
            try:
                img = Image.open(filepath)
                img = img.resize((150, 150))
                photo = ImageTk.PhotoImage(img)
                self.img_label.config(image=photo)
                self.img_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    def save_product(self):
        name = self.name.get()
        price = self.price.get()
        image = self.image.get()
        quantity = self.quantity.get()

        if not (name and price and image and quantity):
            messagebox.showwarning("Warning", "Please fill in all fields")
            return

        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and quantity a positive integer")
            return

        try:
            add_product(self.mydb, self.cursor, name, price, image, quantity)
            messagebox.showinfo("Success", "Product added successfully!")
            self.destroy()
            HomeWindow(self.master, self.mydb, self.cursor)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product:\n{e}")

    def go_back(self):
        self.destroy()
        HomeWindow(self.master, self.mydb, self.cursor)

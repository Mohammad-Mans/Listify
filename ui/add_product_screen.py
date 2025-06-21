import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from database import add_product
from .home_screen import HomeWindow  

def add_product_screen(root, mydb, cursor):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Add New Product")
    root.geometry("400x550")
    root.configure(bg="#d8c4ba")

    tk.Label(root, text="Add Product", font=("Arial", 18, "bold"), bg="#d8c4ba").pack(pady=20)

    tk.Label(root, text="Product Name:", bg="#d8c4ba").pack()
    entry_name = tk.Entry(root, width=30)
    entry_name.pack()

    tk.Label(root, text="Price:", bg="#d8c4ba").pack()
    entry_price = tk.Entry(root, width=30)
    entry_price.pack()

    tk.Label(root, text="Quantity:", bg="#d8c4ba").pack()
    entry_quantity = tk.Entry(root, width=30)
    entry_quantity.pack()

    tk.Label(root, text="Product Image:", bg="#d8c4ba").pack(pady=(10, 0))
    entry_image = tk.Entry(root, width=30)
    entry_image.pack()

    img_label = tk.Label(root, bg="#d8c4ba")
    img_label.pack(pady=10)

    def choose_image():
        filepath = filedialog.askopenfilename(
            title="Select Product Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if filepath:
            entry_image.delete(0, tk.END)
            entry_image.insert(0, filepath)
            try:
                img = Image.open(filepath)
                img = img.resize((150, 150))
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                img_label.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{e}")

    tk.Button(root, text="Choose Image from Device", command=choose_image, width=25).pack()

    def save_product():
        name = entry_name.get().strip()
        price = entry_price.get().strip()
        image = entry_image.get().strip()
        quantity = entry_quantity.get().strip()

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
            add_product(mydb, cursor, name, price, image, quantity)
            messagebox.showinfo("Success", "Product added successfully!")
            for widget in root.winfo_children():
                widget.destroy()
            HomeWindow(root, mydb, cursor)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product:\n{e}")
            
    def go_back():
        for widget in root.winfo_children():
            widget.destroy()
        HomeWindow(root, mydb, cursor)


    tk.Button(root, text="Save Product", bg="#4caf50", fg="white", width=20, height=2, command=save_product).pack(pady=15)
    tk.Button(root, text="Back", bg="#c5a491", width=20, height=2, command=go_back).pack()


import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import database
from database import (
    logout,
    get_products,
    increase_product_quantity,
    decrease_product_quantity,
    generate_report_pdf,
    delete_product
)

class HomeWindow(tk.Frame):
    def __init__(self, master, mydb, cursor):
        super().__init__(master, bg="#d8c4ba")
        self.master = master
        self.mydb = mydb
        self.cursor = cursor
        self.user = database.current_seller
        self.pack(fill="both", expand=True)
        self.master.title("Home Screen")
        self.master.geometry("800x600")

        self.create_ui()

    def create_ui(self):
        tk.Label(self, text=self.user["store_name"], font=("Arial", 22, "bold"), bg="#d8c4ba").pack(pady=10)

        top_buttons = tk.Frame(self, bg="#d8c4ba")
        top_buttons.pack(pady=5)

        tk.Button(top_buttons, text="➕ Add Product", command=self.insert_product, width=15).pack(side="left", padx=5)
        tk.Button(top_buttons, text="View Report", command=self.show_report, width=15).pack(side="left", padx=5)
        tk.Button(top_buttons, text="Logout", command=self.logout_user, width=15).pack(side="left", padx=5)

        self.canvas = tk.Canvas(self, bg="#d8c4ba", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.container = tk.Frame(self.canvas, bg="#d8c4ba")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.product_frames = []
        self.refresh_products()

    def refresh_products(self):
        for frame in self.product_frames:
            frame.destroy()
        self.product_frames.clear()

        products = get_products(self.cursor)

        for product in products:
            frame = tk.Frame(self.container, bg="white", bd=2, relief="groove", padx=10, pady=10)
            self.product_frames.append(frame)

            # Load Image
            try:
                img = Image.open(product["image"])
                img = img.resize((130, 130))
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=photo, bg="white")
                label.image = photo
                label.grid(row=0, column=0, rowspan=4)
            except:
                tk.Label(frame, text="Image not found", bg="white").grid(row=0, column=0, rowspan=4)

            tk.Label(frame, text=product["name"], bg="white", font=("Arial", 12)).grid(row=0, column=1, sticky="w")
            tk.Label(frame, text=f"Price: {product['price']}", bg="white", font=("Arial", 10)).grid(row=1, column=1, sticky="w")

            quantity_var = tk.IntVar(value=product["quantity"])
            tk.Label(frame, text="Quantity:", bg="white").grid(row=2, column=1, sticky="w")
            tk.Label(frame, textvariable=quantity_var, bg="white").grid(row=2, column=2)

            tk.Button(frame, text="+", width=3, command=lambda p=product, q=quantity_var: self.update_quantity(p["id"], q, +1)).grid(row=2, column=3)
            tk.Button(frame, text="-", width=3, command=lambda p=product, q=quantity_var: self.update_quantity(p["id"], q, -1)).grid(row=2, column=4)

            tk.Button(frame, text="Delete", bg="red", fg="white", command=lambda p=product: self.delete_product(p)).grid(row=3, column=1, columnspan=2, pady=5)

            frame.pack(padx=10, pady=10, fill="x")

        self.container.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_quantity(self, product_id, quantity_var, change):
        new_qty = quantity_var.get() + change
        if new_qty < 0:
            return
        if change > 0:
            increase_product_quantity(self.mydb, self.cursor, product_id)
        else:
            decrease_product_quantity(self.mydb, self.cursor, product_id)
        quantity_var.set(new_qty)

    def delete_product(self, product):
        if messagebox.askyesno("Delete", f"Delete product: {product['name']}?"):
            delete_product(self.mydb, self.cursor, product["id"])
            self.refresh_products()

    def insert_product(self):
        from .add_product_screen import add_product_screen
        self.destroy()
        add_product_screen(self.master, self.mydb, self.cursor)

    def show_report(self):
        try:
            path = generate_report_pdf(self.mydb, self.cursor)
            messagebox.showinfo("Report Generated", f"PDF saved as:\n{os.path.abspath(path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def logout_user(self):
        logout()
        from .welcome_screen import WelcomeWindow
        self.destroy()
        WelcomeWindow(self.master, self.mydb, self.cursor)

# 🛍️ Shop Inventory Management System

A Python-based desktop application with a GUI (Tkinter) that allows sellers to manage their store inventory — including user registration, login, and full control over product listings.

## 📌 Features

- 🧾 **User Authentication**
  - Seller **Signup** and **Login**
  - Secure password storage using **bcrypt**
  
- 🛒 **Inventory Management**
  - Add new products (with name, price, image, quantity)
  - Increase / Decrease product quantity
  - Delete product when it’s out of stock
  - View list of current products

- 📤 **Report Generation**
  - Export a PDF report of available products using **ReportLab**

- 🧑‍💻 **Technologies Used**
  - Python 3.x
  - Tkinter (for GUI)
  - MySQL (for backend database)
  - bcrypt (for password hashing)
  - ReportLab (for PDF reports)

## ▶️ How to Use the App

1. **Set Up the Database Connection**

   Before running the app, update the MySQL password in the `database.py` file:

   ```python
   def initialize_connection():
       mydb = mysql.connector.connect(
           host = "localhost",
           user = "root",
           password = "your_mysql_password"  # ← Replace this line
       )
       cursor = mydb.cursor()
       create_database(cursor)
       create_tables(cursor)
       return mydb, cursor
   ```

2. **Run the Application**

   Launch the main Python script (`main.py`) to start the app.

3. **Register a New User**

   - On the login screen, click on **Sign Up**.
   - Fill in your credentials and create your account.

4. **Start Managing Your Inventory**

   - After logging in, access the **Home Screen**.
   - Use the **Add Product** button to insert new items.
   - Adjust quantities or delete products as needed.
   - Export your product list to PDF when desired.

## 🖼️ Screenshots
| Main Screen | Sign Up Screen |Login Screen|
| ----------- | -------------- | ------------ |
| ![Main Screen](https://i.postimg.cc/05fW07jH/main.png) | ![Sign Up Screen](https://i.postimg.cc/RhXgCx2z/signup.png) | ![Login Screen](https://i.postimg.cc/yxVfz8QP/login.png) |

| Home Screen |
| ------------ |
| ![Home Screen](https://i.postimg.cc/5N2P7jF9/homescreen.png) |

| Add Product Screen | Add Screen |
| ------------------ | ---------- |
| ![Add Product Screen](https://i.postimg.cc/XYZsW-h8T/addproduct.png) | ![Add Screen](https://i.postimg.cc/157vLPpG/add.png) | 

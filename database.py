import bcrypt
import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

current_seller = None

def initialize_connection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234"
    )
    cursor = mydb.cursor()
    create_database(cursor)
    create_tables(cursor)
    
    return mydb , cursor

def create_database(cursor):
    cursor.execute("CREATE DATABASE if not exists listify")
    cursor.execute("USE listify")

def create_tables(cursor):
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]
    
    if "seller" not in tables:
        cursor.execute("""CREATE TABLE seller(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            store_name VARCHAR(100),
            phone VARCHAR(10),
            password VARCHAR(100))
            """)
        
    if "product" not in tables:
        cursor.execute("""CREATE TABLE product(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            image VARCHAR(255) NOT NULL,
            quantity INT DEFAULT 1,
            seller_id INT,
            FOREIGN KEY (seller_id) REFERENCES seller(id))
            """)

def register(mydb, cursor, data):
    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

    sql = "INSERT INTO seller (username, store_name, phone, password) VALUES (%s, %s, %s, %s)"
    val = (data["username"], data["store_name"], data["phone"], hashed_password)
    cursor.execute(sql, val)

    mydb.commit()
    
def login(cursor, data):
    global current_seller
    sql = "SELECT * FROM seller WHERE username = %s"
    val = (data["username"],)
    cursor.execute(sql, val)
    
    result = cursor.fetchone()
    if result is None:
        return False
    
    stored_hash = result[4].encode('utf-8')
    if bcrypt.checkpw(data["password"].encode('utf-8'), stored_hash):
        current_seller = {
            "id": result[0],
            "username": result[1],
            "store_name": result[2],
            "phone": result[3]
        }
        return True
    return False
    
def logout():
    global current_seller
    current_seller = None

def add_product(mydb, cursor, name, price, image, quantity=1):
    if current_seller is None:
        raise Exception("No seller logged in")

    sql = """INSERT INTO product (name, price, image, quantity, seller_id)
             VALUES (%s, %s, %s, %s, %s)"""
    val = (name, price, image, quantity, current_seller["id"])
    cursor.execute(sql, val)
    mydb.commit()

def get_products(cursor):
    if current_seller is None:
        raise Exception("No seller is currently logged in.")

    sql = "SELECT id, name, price, image, quantity FROM product WHERE seller_id = %s"
    val = (current_seller["id"],)
    cursor.execute(sql, val)
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "image": row[3],
            "quantity": row[4],
        }
        for row in rows
    ]

def increase_product_quantity(mydb, cursor, product_id, amount=1):
    sql = "UPDATE product SET quantity = quantity + %s WHERE id = %s AND seller_id = %s"
    val = (amount, product_id, current_seller["id"])
    cursor.execute(sql, val)
    mydb.commit()


def decrease_product_quantity(mydb, cursor, product_id, amount=1):
    cursor.execute(
        "SELECT quantity FROM product WHERE id = %s AND seller_id = %s",
        (product_id, current_seller["id"])
    )
    result = cursor.fetchone()
    if not result:
        raise Exception("Product not found or doesn't belong to current seller.")

    current_quantity = result[0]
    if current_quantity >= amount:
        cursor.execute(
            "UPDATE product SET quantity = quantity - %s WHERE id = %s AND seller_id = %s",
            (amount, product_id, current_seller["id"])
        )
        mydb.commit()
    else:
        raise Exception("Not enough quantity to decrease.")

def delete_product(mydb, cursor, product_id):
    if current_seller is None:
        raise Exception("No seller is currently logged in.")

    cursor.execute(
        "SELECT id FROM product WHERE id = %s AND seller_id = %s",
        (product_id, current_seller["id"])
    )
    result = cursor.fetchone()

    if not result:
        raise Exception("Product not found or does not belong to the current seller.")

    cursor.execute("DELETE FROM product WHERE id = %s AND seller_id = %s", (product_id, current_seller["id"]))
    mydb.commit()
    
def generate_report_pdf(mydb, cursor, file_path="product_report.pdf"):
    if current_seller is None:
        raise Exception("No seller is currently logged in.")

    seller_name = current_seller["store_name"]
    seller_id = current_seller["id"]

    sql = "SELECT name, price, quantity FROM product WHERE seller_id = %s"
    val = (seller_id,)
    cursor = mydb.cursor()
    cursor.execute(sql, val)
    products = cursor.fetchall()

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"{seller_name} - Product Report")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Product Name")
    c.drawString(250, height - 100, "Price")
    c.drawString(350, height - 100, "Quantity")

    y = height - 120
    c.setFont("Helvetica", 11)
    for name, price, quantity in products:
        c.drawString(50, y, str(name))
        c.drawString(250, y, f"${price:.2f}")
        c.drawString(350, y, str(quantity))
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    return file_path
    
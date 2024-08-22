from tkinter import *
from PIL import Image, ImageTk
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from sales import SalesClass
from bill import BillClass
import sqlite3
from tkinter import messagebox
import os
import time


class InventoryManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700+0+0')
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # ========================= TITLE ==================================

        self.icon_title = PhotoImage(file="img/inventory logo.png")
        title = Label(self.root, text="Inventory Management System", font=("times new roman", 40, "bold"), bg="#010c48",
                      image=self.icon_title, compound=LEFT, fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ============ TITLE ENDS HERE ================

        # ====== LOGOUT BUTTON ================

        btn_logout = Button(self.root, command=self.logout_function, text="Logout",
                            font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # ========= LOGOUT BUTTON ENDS HERE ==============

        # ========== DATE & TIME ======================

        self.lbl_date_time = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t "
                                                   "Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d",
                                   fg="white")
        self.lbl_date_time.place(x=0, y=70, relwidth=1, height=30)

        # =============== DATE & TIME ENDS HERE =================

        # ========== SIDEBAR ============================

        self.MenuLogo = Image.open("img/menu logo.jpg")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        sidebar = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        sidebar.place(x=2, y=102, width=200, height=565)

        lbl_MenuLogo = Label(sidebar, image=self.MenuLogo)
        lbl_MenuLogo.pack(side=TOP, fill=X)

        # ======= LABEL MENU ========

        lbl_menu = Label(sidebar, text="Menu", font=("times new roman", 20), bg="#009688")
        lbl_menu.pack(side=TOP, fill=X)

        # ====== LABEL MENU ENDS HERE ====

        # ===== BUTTONS ==========

        btn_employee = Button(sidebar, text="Employee", command=self.employee, font=("times new roman", 20, "bold"),
                              bg="light gray", bd=2,
                              cursor="hand2")
        btn_employee.pack(side=TOP, fill=X)

        btn_supplier = Button(sidebar, text="Supplier", command=self.supplier, font=("times new roman", 20, "bold"),
                              bg="light gray", bd=2,
                              cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)

        btn_category = Button(sidebar, text="Category", command=self.category, font=("times new roman", 20, "bold"),
                              bg="light gray", bd=2,
                              cursor="hand2")
        btn_category.pack(side=TOP, fill=X)

        btn_products = Button(sidebar, text="Products", command=self.product, font=("times new roman", 20, "bold"),
                              bg="light gray", bd=2,
                              cursor="hand2")
        btn_products.pack(side=TOP, fill=X)

        btn_sales = Button(sidebar, text="Sales", command=self.sales, font=("times new roman", 20, "bold"),
                           bg="light gray", bd=2,
                           cursor="hand2")
        btn_sales.pack(side=TOP, fill=X)

        btn_exit = Button(sidebar, text="Exit", font=("times new roman", 20, "bold"), bg="light gray", bd=2,
                          cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)

        # ========= CONTENT ===============

        self.lbl_employee = Label(self.root, text="Total Employee\n [ 0 ]", bg="#33bbf9",
                                  bd=3, relief=RIDGE, font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n [ 0 ]", bg="#ff5722",
                                  bd=3, relief=RIDGE, font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n [ 0 ]", bg="#009688",
                                  bd=3, relief=RIDGE, font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Products\n [ 0 ]", bg="#607d8b",
                                 bd=3, relief=RIDGE, font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n [ 0 ]", bg="#ffc107",
                               bd=3, relief=RIDGE, font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # ====== FOOTER ============

        lbl_footer = (Label(self.root, text="Inventory Management system | Developed by 'NAME HERE'!!! ",
                            font=("times new roman", 17), bg="#4d636d", fg="white"))
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    # ============= EMPLOYEE ================

    def employee(self):
        self.employeeWindow = Toplevel(self.root)
        self.new_obj = EmployeeClass(self.employeeWindow)

    def supplier(self):
        self.supplierWindow = Toplevel(self.root)
        self.new_obj = SupplierClass(self.supplierWindow)

    def category(self):
        self.categoryWindow = Toplevel(self.root)
        self.new_obj = CategoryClass(self.categoryWindow)

    def product(self):
        self.productWindow = Toplevel(self.root)
        self.new_obj = ProductClass(self.productWindow)

    def sales(self):
        self.salesWindow = Toplevel(self.root)
        self.new_obj = SalesClass(self.salesWindow)

    def bill(self):
        self.billWindow = Toplevel(self.root)
        self.new_obj = BillClass(self.billWindow)

    def update_content(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            employees = cur.fetchall()
            self.lbl_employee.config(text=f"Total Employee\n [ {str(len(employees))} ]")

            cur.execute("SELECT * FROM supplier")
            suppliers = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier\n [ {str(len(suppliers))} ]")

            cur.execute("SELECT * FROM category")
            categories = cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n [ {str(len(categories))} ]")

            cur.execute("SELECT * FROM product")
            products = cur.fetchall()
            self.lbl_product.config(text=f"Total Product\n [ {str(len(products))} ]")

            bill = len(os.listdir('bills'))
            self.lbl_sales.config(text=f"Total Sales\n [ {bill} ]")

            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_date_time.config(
                text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_date_time.after(200, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def logout_function(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = InventoryManagement(root)
    root.mainloop()

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class ProductClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x500+220+130')
        self.root.title("Product Details")
        self.root.config(bg="white")
        self.root.focus_force()

        # ============= variables ============

        self.var_pid = StringVar()

        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        self.cat_list = []
        self.sup_list = []

        self.fetch_cat_sup()

        # ====== frame ===========
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)

        # ========= title ============
        title = Label(product_frame, text="Product Details", font=("goudy old style", 15), bg="#0f4d7d",
                      fg="white").pack(side=TOP, fill=X)

        lbl_category = Label(product_frame, text="Category", font=("goudy old style", 15), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_frame, text="Supplier", font=("goudy old style", 15), bg="white").place(x=30,
                                                                                                             y=110)
        lbl_product = Label(product_frame, text="Product", font=("goudy old style", 15), bg="white").place(x=30, y=160)
        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 15), bg="white").place(x=30, y=210)
        lbl_quantity = Label(product_frame, text="Quantity", font=("goudy old style", 15), bg="white").place(x=30,
                                                                                                             y=260)
        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 15), bg="white").place(x=30, y=310)

        # ============= entry ================
        cmb_category = ttk.Combobox(product_frame, justify=CENTER, textvariable=self.var_category, values=self.cat_list,
                                    state='readonly', font=("goudy old style", 15))
        cmb_category.place(x=150, y=60, width=200)
        cmb_category.current(0)

        cmb_supplier = ttk.Combobox(product_frame, justify=CENTER, textvariable=self.var_supplier, values=self.sup_list,
                                    state='readonly',
                                    font=("goudy old style", 15))
        cmb_supplier.place(x=150, y=110, width=200)
        cmb_supplier.current(0)

        txt_name = Entry(product_frame, textvariable=self.var_name, font=("goudy old style", 15),
                            bg="white").place(x=150, y=160, width=200)
        txt_price = Entry(product_frame, textvariable=self.var_price, font=("goudy old style", 15), bg="white").place(
            x=150, y=210, width=200)
        txt_qty = Entry(product_frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="white").place(x=150,
                                                                                                                  y=260,
                                                                                                                  width=200)

        cmb_status = ttk.Combobox(product_frame, justify=CENTER, textvariable=self.var_status,
                                  values=("Active", "Inactive"), state='readonly',
                                  font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # ==== buttons =============

        btn_add = Button(product_frame, text="Save", command=self.add_function, font=("goudy old style", 15),
                         bg="#2196f3",
                         fg="white",
                         cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_frame, text="Update", command=self.update_function, font=("goudy old style", 15),
                            bg="#4caf50",
                            fg="white",
                            cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_frame, text="Delete", command=self.del_function, font=("goudy old style", 15),
                            bg="#f44336", fg="white",
                            cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_frame, text="Clear", command=self.clear_function, font=("goudy old style", 15),
                           bg="#607d8b", fg="white",
                           cursor="hand2").place(x=340, y=400, width=100, height=40)

        # ========= SEARCH FRAME ===========

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        search_frame = LabelFrame(self.root, text="Search Products", font=("goudy old style", 12, "bold"), bd=2,
                                  relief=RIDGE, bg="white")
        search_frame.place(x=480, y=20, width=600, height=80)

        # ======== COMBOBOX ================

        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search_by,
                                  values=("Search by", "Category", "Supplier", "Name"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        # ======== COMBOBOX ENDS HERE ============

        txt_search = Entry(search_frame, textvariable=self.var_search_txt, font=("goudy old style", 15),
                           bg="light yellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(search_frame, text="Search", command=self.search_function, font=("goudy old style", 15),
                            bg="#4caf50", fg="white",
                            cursor="hand2").place(x=410, y=9, width=150, height=30)

        # =============== product DETAILS ====================

        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(p_frame, orient=VERTICAL)
        scroll_x = Scrollbar(p_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(p_frame, columns=("p_id", "Supplier", "Category", "name",
                                                           "price", "qty", "status"),
                                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.ProductTable.yview)
        scroll_x.config(command=self.ProductTable.xview)

        self.ProductTable.heading("p_id", text="Product ID")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Qty")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("p_id", width=90)
        self.ProductTable.column("Supplier", width=100)
        self.ProductTable.column("Category", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)

        self.ProductTable.pack(fill=BOTH, expand=1)

        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show_function()

    # ============== FUNCTIONS ===========

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")

        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            cur.execute("select cat_name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            cur .execute("select sup_name from supplier")
            sup=cur.fetchall()
            if len(sup) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_category.get() == "Select" or self.var_supplier.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "ALL Fields are required!!!", parent=self.root)

            if self.var_category.get() == "Empty" or self.var_supplier.get() == "Empty":
                messagebox.showerror("Error", "Category & Supplier can't be empty. Please register first!!!", parent=self.root)

            else:
                cur.execute("select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Product already exists, Try some different!!!", parent=self.root)

                else:
                    cur.execute(
                        "Insert into product (Category, Supplier, name, price, qty, status) values(?,?,?,?,?,?)",
                        (
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get()
                        ))
                    con.commit()
                    # print("record added")
                    con.close()
                    messagebox.showinfo("Success","Product has been added successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from product")
            rows = cur.fetchall()
            if len(rows) > 0:
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        # print(row)
        self.var_pid.set(row[0])
        self.var_category.set(row[1])
        self.var_supplier.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Please select product from list!!!", parent=self.root)

            else:
                cur.execute("select * from product where p_id=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid!!!",
                                         parent=self.root)
                else:
                    cur.execute(
                        "Update product set Category=?, Supplier=?, name=?, price=?, qty=?, status=? where p_id=?",
                        (
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success","Updated successfully!!!", parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def del_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from the list!!!", parent=self.root)
            else:
                cur.execute("select * from product where p_id=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid, Try some different!!!",
                                         parent=self.root)
                else:
                    operation = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if operation == True:
                        cur.execute("delete from product where p_id=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "deleted successfully!!!")
                    self.clear_function()
                    self.show_function()

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear_function(self):
        self.var_supplier.set("Select")
        self.var_category.set("Select")
        self.var_name.set("")
        self.var_qty.set("")
        self.var_price.set("")
        self.var_pid.set("")
        self.var_status.set("Active")

        self.var_search_txt.set("")
        self.var_search_by.set("Search by")

        self.show_function()

    def search_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_search_by.get() == "Search by":
                messagebox.showerror("Error", "Select search by option", parent=self.root)
            elif self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Empty Field!!!", parent=self.root)
            else:
                cur.execute(
                    "select * from product where " + self.var_search_by.get() + " LIKE '%" + self.var_search_txt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", " No Record Found!!!")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = ProductClass(root)
    root.mainloop()

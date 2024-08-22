from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os, tempfile


class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700+0+0')
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        # ========================= TITLE ==================================

        self.icon_title = PhotoImage(file='img/inventory logo.png')
        title = Label(self.root, text="Inventory Management System", font=("times new roman", 40, "bold"), bg="#010c48",
                      image=self.icon_title, compound=LEFT, fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # ============ TITLE ENDS HERE ================

        # ====== LOGOUT BUTTON ================

        btn_logout = Button(self.root, command=self.logout_function, text="Logout", font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # ========= LOGOUT BUTTON ENDS HERE ==============

        # ========== DATE & TIME ======================

        self.lbl_date_time = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t "
                                                   "Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d",
                                   fg="white")
        self.lbl_date_time.place(x=0, y=70, relwidth=1, height=30)

        # =============== DATE & TIME ENDS HERE =================

        # ========== variables ===========
        self.varsearch = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        self.chk_print = 1

        # ============ frame ==========
        productFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        productFrame.place(x=6, y=110, width=410, height=550)

        p_title = Label(productFrame, text="All Products", font=("goudy old style", 20, "bold"), bg="#262626",
                        fg="white").pack(side=TOP, fill=X)

        productFrame2 = Frame(productFrame, bd=2, relief=RIDGE, bg="white")
        productFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(productFrame2, text="Search Product", font=("times new roman", 15, "bold"), bg="white",
                           fg="green").place(x=2, y=5)
        lbl_product = Label(productFrame2, text="Product", font=("times new roman", 15, "bold"), bg="white").place(x=2,
                                                                                                                   y=45)

        txt_search = Entry(productFrame2, textvariable=self.varsearch, font=("times new roman", 15), bg="white").place(
            x=125, y=47, width=150, height=22)

        btn_search = Button(productFrame2, command=self.search_function, text="Search", font=("goudy old style", 15),
                            bg="#2196f3", fg="white",
                            cursor="hand2").place(x=280, y=45, width=100, height=25)
        btn_show_all = Button(productFrame2, command=self.show_function, text="Show all", font=("goudy old style", 15),
                              bg="#083531", fg="white",
                              cursor="hand2").place(x=280, y=10, width=100, height=25)

        # =============== products DETAILS ====================

        pro_frame = Frame(productFrame, bd=3, relief=RIDGE)
        pro_frame.place(x=2, y=140, width=398, height=385)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(pro_frame, orient=VERTICAL)
        scroll_x = Scrollbar(pro_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(pro_frame, columns=("p_id", "name", "price", "qty", "status"),
                                         yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.ProductTable.yview)
        scroll_x.config(command=self.ProductTable.xview)

        self.ProductTable.heading("p_id", text="ID")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="QTY")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("p_id", width=90)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("qty", width=100)
        self.ProductTable.column("status", width=100)

        # lbl_note = Label(productFrame, anchor='w', text="Note '0' to remove product from the cart!!!", font=("goudy old style", 10), bg="white", fg="red").pack(side=BOTTOM, fill=X)

        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        # ========= customer =================
        cust_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        cust_frame.place(x=420, y=110, width=530, height=70)
        c_title = Label(cust_frame, text="Customers Details", font=("goudy old style", 15), bg="lightgrey").pack(
            side=TOP, fill=X)

        lbl_name = Label(cust_frame, text="Name", font=("times new roman", 15, "bold"), bg="white").place(x=5, y=35)
        txt_search = Entry(cust_frame, textvariable=self.var_name, font=("times new roman", 13), bg="white").place(
            x=80, y=35, width=180)
        lbl_contact = Label(cust_frame, text="Contact #", font=("times new roman", 15, "bold"), bg="white").place(x=270,
                                                                                                                  y=35)
        txt_contact = Entry(cust_frame, textvariable=self.var_contact, font=("times new roman", 13), bg="white").place(
            x=380, y=35, width=140)

        # ====================================
        ct_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        ct_frame.place(x=420, y=190, width=530, height=360)

        # ===============================================

        self.var_cal_input = StringVar()
        calculator_frame = Frame(ct_frame, bd=9, relief=RIDGE, bg="white")
        calculator_frame.place(x=5, y=10, width=268, height=340)

        self.txt_cal_input = Entry(calculator_frame, justify=RIGHT, textvariable=self.var_cal_input, font=("arial", 15),
                                   width=21, bd=10, relief=GROOVE)
        self.txt_cal_input.grid(row=0, columnspan=4)

        btn_7 = Button(calculator_frame, text='7', command=lambda: self.get_input(7), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=1, column=0)
        btn_8 = Button(calculator_frame, text='8', command=lambda: self.get_input(8), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=1, column=1)
        btn_9 = Button(calculator_frame, text="9", command=lambda: self.get_input(9), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(calculator_frame, text="+", command=lambda: self.get_input('+'), font=("arial", 15, 'bold'),
                         bd=5, width=4, pady=10, cursor="hand2").grid(row=1, column=3)

        btn_4 = Button(calculator_frame, text='4', command=lambda: self.get_input(4), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=2, column=0)
        btn_5 = Button(calculator_frame, text='5', command=lambda: self.get_input(5), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=2, column=1)
        btn_6 = Button(calculator_frame, text="6", command=lambda: self.get_input(6), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=2, column=2)
        btn_subtract = Button(calculator_frame, command=lambda: self.get_input('-'), text="-",
                              font=("arial", 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2").grid(row=2, column=3)

        btn_1 = Button(calculator_frame, text='1', command=lambda: self.get_input(1), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=3, column=0)
        btn_2 = Button(calculator_frame, text='2', command=lambda: self.get_input(2), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=3, column=1)
        btn_3 = Button(calculator_frame, text="3", command=lambda: self.get_input(3), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=10, cursor="hand2").grid(row=3, column=2)
        btn_multiply = Button(calculator_frame, command=lambda: self.get_input('*'), text="*",
                              font=("arial", 15, 'bold'), bd=5, width=4, pady=10, cursor="hand2").grid(row=3, column=3)

        btn_0 = Button(calculator_frame, text='0', command=lambda: self.get_input(0), font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=15, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(calculator_frame, text='C', command=self.calculator_clear, font=("arial", 15, 'bold'), bd=5,
                       width=4, pady=15, cursor="hand2").grid(row=4, column=1)
        btn_equal = Button(calculator_frame, text='=', command=self.perform_cal, font=("arial", 15, 'bold'), bd=5,
                           width=4, pady=15, cursor="hand2").grid(row=4, column=2)
        btn_divide = Button(calculator_frame, text='/', command=lambda: self.get_input('/'), font=("arial", 15, 'bold'),
                            bd=5, width=4, pady=15, cursor="hand2").grid(row=4, column=3)

        # ===================================

        self.cart_list = []

        cart_frame = Frame(ct_frame, bd=3, relief=RIDGE)
        cart_frame.place(x=280, y=8, width=245, height=342)
        self.cart_title = Label(cart_frame, text="Cart \tTotal Product: [0]", font=("goudy old style", 15),
                                bg="lightgrey")
        self.cart_title.pack(side=TOP, fill=X)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
        scroll_x = Scrollbar(cart_frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_frame, columns=("p_id", "name", "price", "qty"),
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.CartTable.yview)
        scroll_x.config(command=self.CartTable.xview)

        self.CartTable.heading("p_id", text="ID")
        self.CartTable.heading("name", text="Name")
        self.CartTable.heading("price", text="Price")
        self.CartTable.heading("qty", text="QTY")

        self.CartTable["show"] = "headings"

        self.CartTable.column("p_id", width=20)
        self.CartTable.column("name", width=100)
        self.CartTable.column("price", width=40)
        self.CartTable.column("qty", width=40)

        lbl_note = Label(productFrame, anchor='w', text="Note '0' to remove product from the cart!!!",
                         font=("goudy old style", 10), bg="white", fg="red").pack(side=BOTTOM, fill=X)

        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        # ========== ADD cart widgets====================================================
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_pprice = StringVar()
        self.var_pqty = StringVar()
        self.var_inStock = StringVar()

        cartWidgets_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cartWidgets_frame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(cartWidgets_frame, text="Product Name", font=("goudy old style", 15), bg="white").place(x=5,
                                                                                                                   y=5)
        txt_p_name = Entry(cartWidgets_frame, textvariable=self.var_pname, font=("times new roman", 15), bg="white",
                           state='readonly').place(x=5, y=35, width=190, height=22)

        lbl_p_price = Label(cartWidgets_frame, text="Price", font=("goudy old style", 15), bg="white").place(x=230, y=5)
        txt_p_price = Entry(cartWidgets_frame, textvariable=self.var_pprice, font=("times new roman", 15), bg="white",
                            state='readonly').place(x=230, y=35, width=190, height=22)

        lbl_p_qty = Label(cartWidgets_frame, text="Quantity", font=("goudy old style", 15), bg="white").place(x=430,
                                                                                                              y=5)
        txt_p_qty = Entry(cartWidgets_frame, textvariable=self.var_pqty, font=("times new roman", 15),
                          bg="white").place(x=430, y=35, width=80, height=22)

        self.lbl_instock = Label(cartWidgets_frame, text="In Stock", font=("goudy old style", 15), bg="white")
        self.lbl_instock.place(x=5, y=70)

        btn_clear = Button(cartWidgets_frame, command=self.clear_cart, text="Clear", font=("times new roman", 15), bg="lightgrey",
                           cursor="hand2").place(x=150, y=70, width=150, height=30)
        btn_addCart = Button(cartWidgets_frame, command=self.add_update_cart, text="Add/update cart",
                             font=("times new roman", 15), bg="orange",
                             cursor="hand2").place(x=310, y=70, width=180, height=30)

        # ============ billing area ====================

        bill_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_frame.place(x=953, y=110, width=410, height=410)

        bill_title = Label(bill_frame, text="Customer Bill Area", font=("goudy old style", 20, "bold"), bg="#262626",
                           fg="white").pack(side=TOP, fill=X)

        scrolly = Scrollbar(bill_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(bill_frame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # =============== billing buttons ===================
        bill_menu_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        bill_menu_frame.place(x=953, y=520, width=410, height=140)

        self.lbl_amount = Label(bill_menu_frame, text="Bill Amount \n[0]", font=("goudy old style", 15, "bold"),
                                bg="#3f51b5", fg="white")
        self.lbl_amount.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(bill_menu_frame, text="Discount \n[5%]", font=("goudy old style", 15, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(bill_menu_frame, text="Net Pay\n[0]", font=("goudy old style", 15, "bold"),
                                 bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(bill_menu_frame, command=self.print_bill, cursor="hand2", text="Print", font=("goudy old style", 15, "bold"),
                           bg="lightgreen", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(bill_menu_frame, command=self.clear_all, cursor="hand2", text="Clear", font=("goudy old style", 15, "bold"),
                               bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(bill_menu_frame, command=self.generate_bill, cursor="hand2", text="Generate/Save",
                              font=("goudy old style", 15, "bold"), bg="#009688", fg="white")
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ============= footer ==================

        footer = Label(self.root, text="Inventory Management System | 'STUDENT NAME HERE'",
                       font=("times new roamn", 23), bg="#4d636d", fg="white", bd=0).pack(side=BOTTOM, fill=X)

        self.show_function()
        self.update_date_time()

    # ================ functions ==================

    def get_input(self, num):
        x_num = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(x_num)

    def calculator_clear(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("Select p_id, name, price, qty, status from product WHERE status='Active'")
            rows = cur.fetchall()
            if len(rows) > 0:
                self.ProductTable.delete(*self.ProductTable.get_children())
                for row in rows:
                    self.ProductTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def search_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.varsearch.get() == "":
                messagebox.showerror("Error", "Empty field!!!", parent=self.root)
            else:
                cur.execute(
                    "SELECT p_id, name, price, qty, status FROM product WHERE name LIKE ?",
                    ('%' + self.varsearch.get() + '%' 'AND status="Active"'))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", " No Record Found!!!")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_pprice.set(row[2])
        self.lbl_instock.config(text=f'IN Stock [{str(row[3])}]')
        self.var_inStock.set(row[3])
        self.var_pqty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        content = (self.CartTable.item(f))
        if content and 'values' in content:
            row = content['values']
            self.var_pid.set(row[0])
            self.var_pname.set(row[1])
            self.var_pprice.set(row[2])
            self.var_pqty.set(row[3])
            self.lbl_instock.config(text=f'IN Stock [{str(row[4])}]')
            self.var_inStock.set(row[4])

    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Product field is empty!!!\n Please select Product from the list.",
                                 parent=self.root)
        elif self.var_pqty.get() == '':
            messagebox.showerror("Error", "Quantity field can't be empty!!!", parent=self.root)

        elif self.var_pqty.get() == '':
            messagebox.showerror("Error", "Quantity field can't be empty!!!", parent=self.root)

        elif int(self.var_pqty.get()) > int(self.var_inStock.get()):
            messagebox.showerror("Error", "Invalid Quantity!!!", parent=self.root)

        else:
            # price_calculate = float(int(self.var_pqty.get()) * float(self.var_pprice.get()))
            price_calculate = self.var_pprice.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_calculate, self.var_pqty.get(), self.var_inStock.get()]
            # self.cart_list.append(cart_data)
            # print(self.cart_list)

            # ========= update cart =============
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index_ += 1
            # print(present, index_)
            if present == 'yes':
                op = messagebox.askyesno("Confirm", "Product already present\n Do you want to update?",
                                         parent=self.root)
                if op == True:
                    if self.var_pqty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        # self.cart_list[index_][2] = price_calculate
                        self.cart_list[index_][3] = self.var_pqty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def bill_updates(self):
        self.bill_amt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amt = self.bill_amt + float(row[2]) * int(row[3])
        self.discount = (self.bill_amt * 5) / 100
        self.net_pay = self.bill_amt - self.discount
        self.lbl_amount.config(text=f"Bill Amount\n{str(self.bill_amt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cart_title.config(text=f"Cart \t Total Product:[{str(len(self.cart_list))}]")

    def generate_bill(self):
        if self.var_name.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", f"Customer Details are required!!!", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Empty cart!!!\nAdd Product first.")
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()

            print_bill = open(f'bills/{str(self.invoice)}.txt', 'w')
            print_bill.write(self.txt_bill_area.get('1.0', END))
            print_bill.close()
            messagebox.showinfo("Saved", "Bill generated!!!", parent=self.root)

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_template = f'''
\t\tMutawir-Inventory
\t Phone No. 0614298682 , Multan-60000
{str("="*47)}
Customer Name: {self.var_name.get()}
Ph no. : {self.var_contact.get()}
Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Product Name\t\t\tQTY\tPrice
{str("="*47)}
'''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_template)

    def bill_bottom(self):
        bill_bottom_template = f'''
{str("="*47)}
Bill Amount\t\t\t\tRs.{self.bill_amt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
'''
        self.txt_bill_area.insert(END, bill_bottom_template)

    def bill_middle(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            for row in self.cart_list:
                p_id = row[0]
                name = row[1]
                qty = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'

                price = float(row[2]) * int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, f"\n {name}\t\t\t{qty}\tRs.{price}")

                # ================ update qty in product table ===============
                cur.execute('UPDATE product SET qty=?, status=? WHERE p_id=?', (
                    qty,
                    status,
                    p_id
                ))
                con.commit()
            con.close()
            self.show_function()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_pprice.set('')
        self.var_pqty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_inStock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_name.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cart_title.config(text=f"Cart \t Total Product:[0]")
        self.varsearch.set('')
        self.chk_print = 0

        self.clear_cart()
        self.show_function()
        self.show_cart()

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_date_time.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_date_time.after(200, self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo("Print", "Please wait while printing", parent=self.root)
            new_file_print = tempfile.mktemp('.txt')
            open(new_file_print, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file_print, 'print')

        else:
            messagebox.showerror("Error", "No bill generate to print!!!", parent=self.root)

    def logout_function(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = BillClass(root)
    root.mainloop()

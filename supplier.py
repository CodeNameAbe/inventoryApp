from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class SupplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x500+220+130')
        self.root.title("Supplier Details")
        self.root.config(bg="white")
        self.root.focus_force()

        # ========= VARIABLES ========

        self.var_sup_inv = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        lbl_search = Label(self.root, bg="white", text="Invoice #", font=("goudy old style", 15))
        lbl_search.place(x=700, y=80)

        txt_search = Entry(self.root, textvariable=self.var_search_txt, font=("goudy old style", 15),
                           bg="light yellow")
        txt_search.place(x=800, y=80, width=160)

        btn_search = Button(self.root, text="Search", command=self.search_function, font=("goudy old style", 15),
                            bg="#4caf50", fg="white",
                            cursor="hand2").place(x=980, y=78, width=100, height=30)

        # ====== title ==========
        lbl_title = Label(self.root, text="Supplier Details", font=("goudy old style", 20, "bold"), bg="#0f4d7d",
                          fg="white").place(x=50, y=10, width=1000, height=40)

        # ============== FORM ==========

        # ============row 1 =============

        lbl_sup_inv = Label(self.root, text="Invoice #:", font=("goudy old style", 15), bg="white").place(x=50, y=80)

        txt_sup_inv = Entry(self.root, textvariable=self.var_sup_inv, font=("goudy old style", 15),
                            bg="white").place(
            x=180, y=80, width=180)

        # ========= row 2 ===================

        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 15), bg="white").place(x=50, y=120)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="white").place(
            x=180, y=120, width=180)

        # ============= row 3 ==============

        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white").place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="white").place(
            x=180, y=160, width=180)

        # ========== row 4 ===============

        lbl_desc = Label(self.root, text="Description:", font=("goudy old style", 15), bg="white").place(x=50, y=200)

        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="white")
        self.txt_desc.place(x=180, y=200, width=470, height=150)

        # ================= form buttons ===============

        btn_add = Button(self.root, text="Save", command=self.add_function, font=("goudy old style", 15), bg="#2196f3",
                         fg="white",
                         cursor="hand2").place(x=180, y=370, width=110, height=35)
        btn_update = Button(self.root, text="Update", command=self.update_function, font=("goudy old style", 15),
                            bg="#4caf50",
                            fg="white",
                            cursor="hand2").place(x=300, y=370, width=110, height=35)
        btn_delete = Button(self.root, text="Delete", command=self.del_function, font=("goudy old style", 15),
                            bg="#f44336", fg="white",
                            cursor="hand2").place(x=420, y=370, width=110, height=35)
        btn_clear = Button(self.root, text="Clear", command=self.clear_function, font=("goudy old style", 15),
                           bg="#607d8b", fg="white",
                           cursor="hand2").place(x=540, y=370, width=110, height=35)

        # =============== Supplier DETAILS ====================

        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=700, y=120, width=380, height=350)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(sup_frame, orient=VERTICAL)
        scroll_x = Scrollbar(sup_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(sup_frame, columns=("sup_inv", "sup_name", "sup_contact", "sup_desc"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.SupplierTable.yview)
        scroll_x.config(command=self.SupplierTable.xview)

        self.SupplierTable.heading("sup_inv", text="Supplier ID")
        self.SupplierTable.heading("sup_name", text="Name")
        self.SupplierTable.heading("sup_contact", text="Contact")
        self.SupplierTable.heading("sup_desc", text="Description")

        self.SupplierTable["show"] = "headings"

        self.SupplierTable.column("sup_inv", width=90)
        self.SupplierTable.column("sup_name", width=100)
        self.SupplierTable.column("sup_contact", width=100)
        self.SupplierTable.column("sup_desc", width=100)

        self.SupplierTable.pack(fill=BOTH, expand=1)

        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show_function()

    # ============== FUNCTIONS ===========

    def add_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_sup_inv.get() == "":
                messagebox.showerror("Error", "ID must be required!!!", parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Name must be required!!!")

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Contact must be required!!!")

            else:
                cur.execute("select * from supplier where sup_inv=?", (self.var_sup_inv.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "ID already exists, Try some different!!!", parent=self.root)

                else:
                    cur.execute(
                        "Insert into supplier (sup_inv, sup_name, sup_contact, sup_desc) values(?,?,?,?)",
                        (
                            self.var_sup_inv.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0', END),
                        ))
                    con.commit()
                    # print("record added")
                    con.close()
                    messagebox.showinfo("Success", f"Supplier '{self.var_name.get()}' has been added successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows = cur.fetchall()
            if len(rows) > 0:
                self.SupplierTable.delete(*self.SupplierTable.get_children())
                for row in rows:
                    self.SupplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        # print(row)
        self.var_sup_inv.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    def update_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_sup_inv.get() == "":
                messagebox.showerror("Error", "ID must be required!!!", parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Name must be required!!!")

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "contact must be required!!!")

            else:
                cur.execute("select * from supplier where sup_inv=?", (self.var_sup_inv.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid ID, Try some different!!!",
                                         parent=self.root)

                else:
                    cur.execute(
                        "Update supplier set sup_name=?, sup_contact=?, sup_desc=? where sup_inv=?",
                        (
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0', END),
                            self.var_sup_inv.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success", f"Supplier '{self.var_name.get()}' has been updated successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def del_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_sup_inv.get() == "":
                messagebox.showerror("Error", "ID must be required!!!", parent=self.root)
            else:
                cur.execute("select * from supplier where sup_inv=?", (self.var_sup_inv.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid ID, Try some different!!!",
                                         parent=self.root)
                else:
                    operation = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if operation == True:
                        cur.execute("delete from supplier where sup_inv=?", (self.var_sup_inv.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", f'Supplier "{self.var_sup_inv.get()}" deleted successfully!!!')
                    self.clear_function()
                    self.show_function()

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear_function(self):
        self.var_sup_inv.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0', END)
        self.var_search_txt.set("")

        self.show_function()

    def search_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Empty Field!!!", parent=self.root)
            else:
                cur.execute(
                    "select * from supplier where sup_inv=?", (self.var_search_txt.get(),))
                row = cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", " No Record Found!!!")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = SupplierClass(root)
    root.mainloop()

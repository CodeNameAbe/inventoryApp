from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class CategoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x500+220+130')
        self.root.title("Category")
        self.root.config(bg="white")
        self.root.focus_force()

        # ========== variables =========
        self.var_cat_id = StringVar()
        self.var_cat_name = StringVar()

        # ============ title ===========

        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a54", fg="white").pack(side=TOP, fill=X)
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="white").place(x=50, y=100)
        txt_name = Entry(self.root, textvariable=self.var_cat_name, font=("goudy old style", 18), bg="white").place(x=50, y=170, width=300)

        btn_add = Button(self.root, text="Add", command=self.add_function, font=("goudy old style", 18), bg="#4caf50", fg="white", cursor="hand2").place(x=360, y=170, width=150, height=30)
        btn_del = Button(self.root, text="Delete", command=self.del_function, font=("goudy old style", 18), bg="red", fg="white", cursor="hand2").place(x=520, y=170, width=150, height=30)

        # =========== graphics ==============
        self.img = Image.open("img/category.jpg")
        self.img = self.img.resize((618, 250), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)

        self.lbl_img = Label(self.root, image=self.img)
        self.lbl_img.place(x=50, y=220)

        # =============== treeview ====================

        treeview_frame = Frame(self.root, bd=3, relief=RIDGE)
        treeview_frame.place(x=700, y=70, width=380, height=400)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(treeview_frame, orient=VERTICAL)
        scroll_x = Scrollbar(treeview_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(treeview_frame, columns=("cat_id", "cat_name"), yscrollcommand=scroll_y.set,
                                          xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.CategoryTable.yview)
        scroll_x.config(command=self.CategoryTable.xview)

        self.CategoryTable.heading("cat_id", text="Category ID")
        self.CategoryTable.heading("cat_name", text="Name")

        self.CategoryTable["show"] = "headings"

        self.CategoryTable.column("cat_id", width=90)
        self.CategoryTable.column("cat_name", width=100)

        self.CategoryTable.pack(fill=BOTH, expand=1)

        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        self.show_function()

    # ============= functions ==============
    def add_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_cat_name.get() == "":
                messagebox.showerror("Error", "Name must be required!!!", parent=self.root)

            else:
                cur.execute("select * from category where cat_name=?", (self.var_cat_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Category already exists, Try some different!!!", parent=self.root)

                else:
                    cur.execute(
                        "Insert into category (cat_name) values(?)",(self.var_cat_name.get(),))
                    con.commit()
                    # print("record added")
                    con.close()
                    messagebox.showinfo("Success", f"Category '{self.var_cat_name.get()}' has been added successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from category")
            rows = cur.fetchall()
            if len(rows) > 0:
                self.CategoryTable.delete(*self.CategoryTable.get_children())
                for row in rows:
                    self.CategoryTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = (self.CategoryTable.item(f))
        row = content['values']
        # print(row)
        self.var_cat_id.set(row[0])
        self.var_cat_name.set(row[1])

    def del_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "ID must be required!!!", parent=self.root)
            else:
                cur.execute("select * from category where cat_id=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid ID, Try some different!!!",
                                         parent=self.root)
                else:
                    operation = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if operation == True:
                        cur.execute("delete from category where cat_id=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", f'Supplier "{self.var_cat_id.get()}" deleted successfully!!!')
                    self.clear_function()
                    self.show_function()

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear_function(self):
        self.var_cat_id.set("")
        self.var_cat_name.set("")

        self.show_function()


if __name__ == "__main__":
    root = Tk()
    obj = CategoryClass(root)
    root.mainloop()

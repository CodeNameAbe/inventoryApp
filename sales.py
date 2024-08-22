from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os


class SalesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x500+220+130')
        self.root.title("Sales Details")
        self.root.config(bg="white")
        self.root.focus_force()

        # ======== variable ===========
        self.var_invoice = StringVar()
        self.bill_list = []

        # =========== title ===========
        lbl_title = Label(self.root, text="View Customer Bills", font=("goudy old style", 30), bg="#184a45", fg="white",
        bd=3, relief=RIDGE).pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_inv = Label(self.root, text="Invoice #", font=("times new roman", 15), bg="white").place(x=50, y=100)
        self.txt_inv = Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="white").place(x=160, y=100, width=180, height=28)

        btn_search = Button(self.root, text="Search", command=self.search_function, font=("times new roman", 15, "bold"), cursor="hand2", bg="#2196f3", fg="white").place(x=360, y=100, width=120, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear_function, font=("times new roman", 15, "bold"), cursor="hand2", bg="lightgrey").place(x=490, y=100, width=120, height=28)

        sales_frame = Frame(self.root, bd=2, relief=RIDGE)
        sales_frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_frame ,orient=VERTICAL)

        self.sales_list = Listbox(sales_frame, font=("goudy old style", 15), bg="white")

        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)

        self.sales_list.pack(fill=BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # ====================

        bill_frame = Frame(self.root, bd=2, relief=RIDGE)
        bill_frame.place(x=280, y=140, width=410, height=330)

        lbl_title = Label(bill_frame, text="View Customer Bills", font=("goudy old style", 30), bg="orange").pack(
            side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)

        self.bill_area = Text(bill_frame, bg="white")

        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)

        self.bill_area.pack(fill=BOTH, expand=1)

        # ============ img ===============

        self.bill_img = Image.open("img/cat2.jpg")
        self.bill_img = self.bill_img.resize((380, 355), Image.LANCZOS)
        self.bill_img = ImageTk.PhotoImage(self.bill_img)
        lbl_img = Label(self.root, image=self.bill_img)
        lbl_img.place(x=700, y=110)

        self.show_function()

    # ========= functions ============
    def show_function(self):
        del self.bill_list[:]
        self.sales_list.delete(0, END)
        for i in os.listdir('bills'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index_ = self.sales_list.curselection()
        file_name = self.sales_list.get(index_)
        print(file_name)
        self.bill_area.delete('1.0', END)
        fp = open(f'bills/{file_name}', 'r')
        for i in fp:
            self.bill_area.insert(END, i)
        fp.close()

    def search_function(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice # required", parent= self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bills/{self.var_invoice.get()}.txt', 'r')
                self.bill_area.delete('1.0', END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error", "INvalid Invoice", parent=self.root)

    def clear_function(self):
        self.show_function()
        self.bill_area.delete('1.0', END)


if __name__ == "__main__":
    root = Tk()
    obj = SalesClass(root)
    root.mainloop()

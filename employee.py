from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class EmployeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x500+220+130')
        self.root.title("Employee Details")
        self.root.config(bg="white")
        self.root.focus_force()

        # ========= VARIABLES ========

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_user_type = StringVar()
        self.var_salary = StringVar()
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        # ========= SEARCH FRAME ===========

        search_frame = LabelFrame(self.root, text="Search Employee", font=("goudy old style", 12, "bold"), bd=2,
                                  relief=RIDGE, bg="white")
        search_frame.place(x=250, y=20, width=600, height=70)

        # ======== COMBOBOX ================

        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_search_by,
                                  values=("Search by", "emp_id", "emp_name", "emp_email", "emp_contact"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        # ======== COMBOBOX ENDS HERE ============

        txt_search = Entry(search_frame, textvariable=self.var_search_txt, font=("goudy old style", 15),
                           bg="light yellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(search_frame, text="Search", command=self.search_function, font=("goudy old style", 15), bg="#4caf50", fg="white",
                            cursor="hand2").place(x=410, y=9, width=150, height=30)

        # ====== title ==========
        lbl_title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d",
                          fg="white").place(x=50, y=100, width=1000)

        # ============== FORM ==========

        # ============row 1 =============

        lbl_emp_id = Label(self.root, text="Employee ID:", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender:", font=("goudy old style", 15), bg="white").place(x=370, y=150)
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        self.txt_emp_id = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15),
                           bg="white").place(
            x=170, y=150, width=180)

        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,
                                  values=("Select", "Male", "Female", "Other"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="white").place(
            x=850, y=150, width=180)

        # ========= row 2 ===================

        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="DOB:", font=("goudy old style", 15), bg="white").place(x=370, y=190)
        lbl_doj = Label(self.root, text="DOJ:", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="white").place(
            x=170, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="white").place(
            x=500, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="white").place(
            x=850, y=190, width=180)

        # ============= row 3 ==============

        lbl_email = Label(self.root, text="E-Mail:", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_password = Label(self.root, text="Password:", font=("goudy old style", 15), bg="white").place(x=370, y=230)
        lbl_user_type = Label(self.root, text="User Type:", font=("goudy old style", 15), bg="white").place(x=750,
                                                                                                            y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="white").place(
            x=170, y=230, width=180)
        txt_password = Entry(self.root, textvariable=self.var_password, font=("goudy old style", 15), bg="white").place(
            x=500, y=230, width=180)

        cmb_user_type = ttk.Combobox(self.root, textvariable=self.var_user_type,
                                     values=("Admin", "Employee"), state="readonly", justify=CENTER,
                                     font=("goudy old style", 15))
        cmb_user_type.place(x=850, y=230, width=180)
        cmb_user_type.current(0)

        # ========== row 4 ===============

        lbl_address = Label(self.root, text="Address:", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary:", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="white")
        self.txt_address.place(x=170, y=270, width=300, height=60)
        txt_salary = Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="white").place(
            x=600, y=270, width=180)

        # ================= form buttons ===============

        btn_add = Button(self.root, text="Save", command=self.add_function, font=("goudy old style", 15), bg="#2196f3",
                         fg="white",
                         cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update", command=self.update_function, font=("goudy old style", 15),
                            bg="#4caf50",
                            fg="white",
                            cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.del_function, font=("goudy old style", 15),
                            bg="#f44336", fg="white",
                            cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear_function, font=("goudy old style", 15), bg="#607d8b", fg="white",
                           cursor="hand2").place(x=860, y=305, width=110, height=28)

        # =============== EMPLOYEE DETAILS ====================

        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        # ======== scroll bar ===============

        scroll_y = Scrollbar(emp_frame, orient=VERTICAL)
        scroll_x = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("emp_id", "emp_name", "emp_email", "emp_gender",
                                                              "emp_contact", "emp_dob", "emp_doj", "emp_password",
                                                              "emp_user_type", "emp_address", "emp_salary"),
                                          yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.EmployeeTable.yview)
        scroll_x.config(command=self.EmployeeTable.xview)

        self.EmployeeTable.heading("emp_id", text="Employee ID")
        self.EmployeeTable.heading("emp_name", text="Name")
        self.EmployeeTable.heading("emp_email", text="E-Mail")
        self.EmployeeTable.heading("emp_gender", text="Gender")
        self.EmployeeTable.heading("emp_contact", text="Contact")
        self.EmployeeTable.heading("emp_dob", text="D.O.B")
        self.EmployeeTable.heading("emp_doj", text="D.O.J")
        self.EmployeeTable.heading("emp_password", text="Password")
        self.EmployeeTable.heading("emp_user_type", text="User Type")
        self.EmployeeTable.heading("emp_address", text="Address")
        self.EmployeeTable.heading("emp_salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("emp_id", width=90)
        self.EmployeeTable.column("emp_name", width=100)
        self.EmployeeTable.column("emp_email", width=100)
        self.EmployeeTable.column("emp_gender", width=100)
        self.EmployeeTable.column("emp_contact", width=100)
        self.EmployeeTable.column("emp_dob", width=100)
        self.EmployeeTable.column("emp_doj", width=100)
        self.EmployeeTable.column("emp_password", width=100)
        self.EmployeeTable.column("emp_user_type", width=100)
        self.EmployeeTable.column("emp_address", width=200)
        self.EmployeeTable.column("emp_salary", width=100)

        self.EmployeeTable.pack(fill=BOTH, expand=1)

        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show_function()

    # ============== FUNCTIONS ===========

    def add_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!!!", parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Employee Name must be required!!!")

            elif self.var_email.get() == "":
                messagebox.showerror("Error", "Employee email must be required!!!")

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Employee contact must be required!!!")

            elif self.var_dob.get() == "":
                messagebox.showerror("Error", "Employee dob must be required!!!")

            elif self.var_doj.get() == "":
                messagebox.showerror("Error", "Employee doj must be required!!!")

            elif self.var_password.get() == "":
                messagebox.showerror("Error", "Employee password must be required!!!")

            elif self.var_salary.get() == "":
                messagebox.showerror("Error", "Employee Salary must be required!!!")

            else:
                cur.execute("select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "ID already exists, Try some different!!!", parent=self.root)

                else:
                    cur.execute(
                        "Insert into employee (emp_id, emp_name, emp_email, emp_gender, emp_contact, emp_dob, emp_doj, emp_password, emp_user_type, emp_address, emp_salary) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_password.get(),
                            self.var_user_type.get(),
                            self.txt_address.get('1.0', END),
                            self.var_salary.get()
                        ))
                    con.commit()
                    # print("record added")
                    con.close()
                    messagebox.showinfo("Success", f"Employee '{self.var_name.get()}' has been added successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def show_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from employee")
            rows = cur.fetchall()
            if len(rows) > 0:
                self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                for row in rows:
                    self.EmployeeTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']
        # print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_password.set(row[7])
        self.var_user_type.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    def update_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!!!", parent=self.root)

            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Employee Name must be required!!!")

            elif self.var_email.get() == "":
                messagebox.showerror("Error", "Employee email must be required!!!")

            elif self.var_contact.get() == "":
                messagebox.showerror("Error", "Employee contact must be required!!!")

            elif self.var_dob.get() == "":
                messagebox.showerror("Error", "Employee dob must be required!!!")

            elif self.var_doj.get() == "":
                messagebox.showerror("Error", "Employee doj must be required!!!")

            elif self.var_password.get() == "":
                messagebox.showerror("Error", "Employee password must be required!!!")

            elif self.var_salary.get() == "":
                messagebox.showerror("Error", "Employee Salary must be required!!!")

            else:
                cur.execute("select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID, Try some different!!!",
                                         parent=self.root)

                else:
                    cur.execute(
                        "Update employee set emp_name=?, emp_email=?, emp_gender=?, emp_contact=?, emp_dob=?, emp_doj=?, emp_password=?, emp_user_type=?, emp_address=?, emp_salary=? where emp_id=?",
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_password.get(),
                            self.var_user_type.get(),
                            self.txt_address.get('1.0', END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                        ))
                    con.commit()
                    messagebox.showinfo("Success", f"Employee '{self.var_name.get()}' has been updated successfully!!!",
                                        parent=self.root)
                    self.show_function()
                    self.clear_function()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def del_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required!!!", parent=self.root)
            else:
                cur.execute("select * from employee where emp_id=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID, Try some different!!!",
                                         parent=self.root)
                else:
                    operation = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if operation == True:
                        cur.execute("delete from employee where emp_id=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", f'Employee "{self.var_emp_id.get()}" deleted successfully!!!')
                    self.clear_function()
                    self.show_function()

        except EXCEPTION as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def clear_function(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_password.set("")
        self.var_user_type.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
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
                    "select * from employee where " + self.var_search_by.get() + " LIKE '%" + self.var_search_txt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", " No Record Found!!!")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = EmployeeClass(root)
    root.mainloop()

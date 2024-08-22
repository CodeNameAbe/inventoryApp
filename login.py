import sqlite3
from tkinter import *
from tkinter import messagebox
import os
import email_pass
import smtplib
import time


class Login_Wala_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700+0+0')
        self.root.title("Login System")
        self.root.config(bg="white")

        self.otp = ''

        # =======================================
        self.employee_id = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        login_frame.place(x=260, y=90, width=350, height=460)

        Label(login_frame, text="Login System", bg="white", font=("Elephant", 30, "bold")).place(x=0, y=30, relwidth=1)

        Label(login_frame, text="Employee ID ", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=120)

        Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=150,
                                                                                                            width=250)

        Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)

        Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=230, width=250)

        Button(login_frame, command=self.login_function, text="Log In", font=("Arial Rounded MT Bold", 15),
               bg="#00B0F0", cursor="hand2").place(x=50,
                                                   y=300,
                                                   width=250,
                                                   height=35)

        Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)

        Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150,
                                                                                                              y=357)

        Button(login_frame, text="Forgot Password?", command=self.forget_window, bd=0, activebackground="white",
               activeforeground="#00759E",
               font=("times new roman", 13), bg="white", fg="#00759E").place(x=100, y=395)

    def login_function(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required!!!", parent=self.root)
            else:
                cur.execute("SELECT emp_user_type FROM employee WHERE emp_id=? AND emp_password=?",
                            (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid username/password", parent=self.root)
                else:
                    # print(user)
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python bill.py")
        except Exception as es:
            messagebox.showerror("Error", f"error due to : {str(es)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r'db_inventory.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Empty field!!!")
            else:
                cur.execute("SELECT emp_email FROM employee WHERE emp_id=?",
                            (self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid ID!!! \n Try again.", parent=self.root)
                else:
                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title("RESET PASSWORD")
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()

                    # ========= variables ==================
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_confirm_password = StringVar()
                    chk = self.send_email(email[0])
                    if chk != 'f':
                        messagebox.showerror("Error", "connection error, Try again!!!", parent=self.root)
                    else:
                        Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, "bold"),
                              bg="#3f51b5", fg="white").pack(side=TOP, fill=X)
                        Label(self.forget_win, text="Enter OTP sent on ur registered mail",
                              font=("times new roman", 15)).place(x=20, y=60)

                        self.var_otp_entry = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15),
                              bg="light yellow").place(x=20, y=100)

                        self.btn_reset = Button(self.forget_win, command=self.validate_otp, text="Submit", font=("times new roman", 15), bg='lightgray')
                        self.btn_reset.place(x=250, y=98, width=100, height=30)

                        Label(self.forget_win, text="New password",
                              font=("times new roman", 15)).place(x=20, y=160)

                        Entry(self.forget_win, textvariable=self.var_new_pass,
                              font=("tims new roman", 15),
                              bg="light yellow").place(x=20, y=190)

                        Label(self.forget_win, text="confirm password",
                              font=("times new roman", 15)).place(x=20, y=225)

                        Entry(self.forget_win, textvariable=self.var_confirm_password,
                              font=("tims new roman", 15),
                              bg="light yellow").place(x=20, y=255)

                        self.btn_update = Button(self.forget_win, command=self.update_password, state=DISABLED, text="Update", font=("times new roman", 15),
                                            bg='light gray')
                        self.btn_update.place(x=150, y=300, width=100, height=30)
        except Exception as es:
            messagebox.showerror("Error", f"Error due to : {str(es)}", parent=self.root)

    def send_email(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_pass.email_
        pass_ = email_pass.pass_

        s.login(email_, pass_)

        self.otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
        subj = 'Reset password OTP'
        msg = f'Dear Sir/Madam, \n\nYour OTP is {str(self.otp)}. \n\n with Regards,\n Mutawir'
        msg = "Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)
        chk = s.ehlo()
        if chk == 250:
            return 's'
        else:
            return 'f'

    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error", "Invalid OTP, Try again!!!", parent=self.forget_win)

    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_confirm_password.get() == "":
            messagebox.showerror("Error", "Empty fields!!!", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_confirm_password.get():
            messagebox.showerror("Error", "Password didn't match!!!", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'db_inventory.db')
            cur = con.cursor()
            try:
                cur.execute("UPDATE employee SET emp_password=? WHERE emp_id=?", (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully!!!")
                self.forget_win.destroy()
            except Exception as es:
                messagebox.showerror("Error", f"Error due to {str(es)}", parent=self.forget_win)


if __name__ == "__main__":
    root = Tk()
    obj = Login_Wala_System(root)
    root.mainloop()

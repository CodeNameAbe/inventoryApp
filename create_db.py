import sqlite3


def create_db():
    con = sqlite3.connect('db_inventory.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(emp_id INTEGER PRIMARY KEY AUTOINCREMENT, emp_name text,"
                "emp_email text, emp_gender text, emp_contact text, emp_dob text, emp_doj text, emp_password text,"
                "emp_user_type text, emp_address text, emp_salary text)")
    con.commit()
    # print('success')

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(sup_inv INTEGER PRIMARY KEY AUTOINCREMENT, sup_name text,"
                "sup_contact text, sup_desc text)")
    con.commit()
    # print('success')

    cur.execute("CREATE TABLE IF NOT EXISTS category(cat_id INTEGER PRIMARY KEY AUTOINCREMENT, cat_name text)")
    con.commit()
    # print('success')

    cur.execute("CREATE TABLE IF NOT EXISTS product(p_id INTEGER PRIMARY KEY AUTOINCREMENT, Supplier text,"
                "Category text, name text, price text, qty text, status text)")
    con.commit()
    # print('success')


create_db()

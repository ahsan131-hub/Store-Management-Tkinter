import datetime

import sqlite3
from sqlite3 import Error
from tkinter import messagebox

try:
    sqliteConnection = sqlite3.connect('SQLite_Python.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    # sql_create_customer_table = """CREATE TABLE IF NOT EXISTS customers (
    #                                 id integer PRIMARY KEY  ,
    #                                 mobile_no text NOT NULL,
    #                                 customer_name integer,
    #                                 email message_text NOT NULL
    #                             );"""

    sql_emp_table = """CREATE TABLE IF NOT EXISTS employees (
                                        id integer PRIMARY KEY  ,
                                        name text NOT NULL,
                                        phone text,
                                        cnic message_text NOT NULL,
                                        address integer NOT NULL,
                                        salary integer ,
                                        loan integer                             
                                    );"""


    sql_product_table = """CREATE TABLE IF NOT EXISTS products (
                                      id integer PRIMARY KEY,
                                      product_name text NOT NULL,
                                      product_gauge integer,
                                      product_weight integer ,
                                      product_quantity integer ,
                                      product_purchase_price integer ,
                                      product_sale_price integer 

                       
                                  );"""
    # entry_mob, custName, txtemail,self.subtotal, discount,txt_total,pending_amount, date_time
    sql_billcounter_table = """CREATE TABLE IF NOT EXISTS billcounter (
                                      id integer PRIMARY KEY,
                                      mobile_no message_text ,
                                      customer_name message_text ,
                                      email message_text ,
                                       products message_text,
                                      sub_total integer NOT NULL,
                                      total integer NOT NULL,
                                      discount integer ,
                                      pending_amount integer ,
                                      paid  integer,
                                      return_amt integer,
                                      credit_amount integer,
                                      dateTime current_date
                                                               
                                  );"""

    # cursor.execute(sql_create_customer_table)
    cursor.execute(sql_billcounter_table)
    cursor.execute(sql_product_table)
    cursor.execute(sql_emp_table)
    # FOREIGNcu
    # KEY(project_id)
    # REFERENCES
    # projects(id)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


def add_customer(data):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = """INSERT INTO customers
                                    (mobile_no,customer_name,email) 
                                    VALUES (?, ?, ?);"""
        c.execute(sql, data)
        conn.commit()
        print("employeee added")
        return c.lastrowid
    except Error as e:
        print("error", e)

def get_customers():
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = """SELECT	customer_name,mobile_no,SUM(total) total,SUM(pending_amount) pending,SUM(paid) total_paid,SUM(credit_amount) credit FROM billcounter GROUP BY mobile_no;"""
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print("employeee added")
        return rows
    except Error as e:
        print("error", e)


def add_billcounter(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = """INSERT INTO billcounter (mobile_no,customer_name,email,products,sub_total,total,discount,pending_amount,paid,return_amt,credit_amount,dateTime) 
                                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""
        c.execute(sql, data)
        print(c.fetchall())
        conn.commit()
        messagebox.showinfo("Bill Save ", "Bill Saved")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Bill Not Save ", "Bill not Saved")
        print("error", e)



def add_employee(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = """INSERT INTO employees (name,phone,cnic,address,salary,loan) 
                                               VALUES (?, ?, ?,?,?,?);"""
        c.execute(sql, data)
        rows=c.fetchall()
        conn.commit()
        print("employeee added")
        messagebox.showinfo("Employee ", "New Employee Added")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Error", "Cannot add Employee")
        print("error", e)



def update_employee(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        print(data)
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Update employees set name="+"'"+data[1]+"',"+"phone="+"'"+data[2]+"',"+"cnic="+"'"+data[3]+"',"+"address="+"'"+data[4]+"',"+"salary="+"'"+data[5]+"',"+"loan="+"'"+data[6]+"'"+"where id="+data[0]+";"
        c.execute(sql)
        print("updated employees")
        conn.commit()
        messagebox.showinfo("Employee ", " Employee Updated")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Error", "Cannot Update Employee")
        print("error", e)


def delete_employee(data):
    try:
        print(data)
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Delete from employees where id="+data[0]+";"
        c.execute(sql)
        print("deleted employees")
        conn.commit()
        messagebox.showinfo("Employee ", " Employee deleted")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Error", "Cannot Delete Employee")
        print("error", e)


def get_employees():
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = """select * from employees"""
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)



def get_bills():
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = """select * from billcounter"""
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)

def get_bill_by_id(id):
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "select * from billcounter where id ='"+str(id)+"'"
        c.execute(sql)
        # if(len(c.fetchall()) <=0):
        #     return ()
        rows=c.fetchall()[0]
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)

def get_bills_by_date(date):
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql ="select * from billcounter where dateTime='"+date+"';"
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)

def get_bills_by_phone(phone):
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql ="select * from billcounter where mobile_no='"+phone+"';"
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)


def add_product(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = """INSERT INTO products (product_name,product_gauge,product_weight,product_quantity,product_purchase_price,product_sale_price) 
                                               VALUES (?,?,?,?,?,?);"""
        c.execute(sql, data)
        # rows=c.fetchall()
        conn.commit()
        print("pproduct is added")
        return c.lastrowid
    except Error as e:
        print("error", e)

def update_product(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        print(data)
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Update products set product_name="+"'"+data[1]+"',"+"product_gauge="+"'"+data[2]+"',"+"product_weight="+"'"+data[3]+"',"+"product_quantity="+"'"+data[4]+"',"+"product_purchase_price="+"'"+data[5]+"',"+"product_sale_price="+"'"+data[6]+"'"+"where id="+data[0]+";"
        c.execute(sql)
        print("updated")
        conn.commit()
        return c.lastrowid
    except Error as e:
        print("error", e)

def get_stocks():
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = """select * from products"""
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows
    except Error as e:
        print("error", e)
def get_product_quantity(id):
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = "select product_quantity from products where id='"+id+"';"
        c.execute(sql)
        quantity=c.fetchall()[0][0]
        conn.commit()
        print("quantity",quantity)
        return quantity
    except Error as e:
        print("error", e)


def get_product(id):
    """
    Create a new billcounter
    :param conn:"'"+
    :p+"'"aram task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()

        sql = "select * from products where id="+id
        c.execute(sql)
        rows=c.fetchall()
        conn.commit()
        print(rows)
        return rows[0]
    except Error as e:
        print("error", e)


def modify_product(data):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        print(data[1], data[0])
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Update products set product_quantity=(products.product_quantity-" + data[1] + ") where product_name='" + \
              data[0] + "';"
        c.execute(sql)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print("error", e)



def get_daily_profit():
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        yesterday=(datetime.datetime.today() - datetime.timedelta(days = 1)).date()
        print(str(yesterday))
        sql = "select * from billcounter where dateTime='"+str(yesterday)+"';"
        c.execute(sql)
        rows = c.fetchall()
        print(rows)
        sale = 0
        pending=0
        for row in rows:
            sale += row[6]
            pending+=row[8]
            print(row[5])
        conn.commit()
        return (pending,sale,rows)
    except Error as e:
        print("error", e)

def update_pending_amount(id,amount):
    try:
        print(id,amount)
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Select total, pending_amount from billcounter where id=" + str(id) + ";"
        c.execute(sql)
        row=c.fetchall()[0]
        print(row)
        total=row[0]
        pending=row[1]-amount
        sql = "Update billcounter set pending_amount="+"'"+str(pending)+"',total="+"'"+str(total)+"' where id="+str(id)+";"
        c.execute(sql)
        print("updated amount")
        conn.commit()
        messagebox.showinfo("amount updated", " amount updated")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Error", "Cannot Update amount")
        print("error", e)


def update_credit_amount(id,amount):
    try:
        print(id,amount)
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "Select return_amt, credit_amount from billcounter where id=" + str(id) + ";"
        c.execute(sql)
        row=c.fetchall()[0]
        print(row)
        return_amt=row[0]+amount
        credit_amount=row[1]-amount
        sql = "Update billcounter set credit_amount="+"'"+str(credit_amount)+"',return_amt="+"'"+str(return_amt)+"' where id="+str(id)+";"
        c.execute(sql)
        print("updated amount")
        conn.commit()
        messagebox.showinfo("amount updated", " credeited updated")
        return c.lastrowid
    except Error as e:
        messagebox.showerror("Error", "Cannot Update amount")
        print("error", e)

def get_monthly_profit():
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = """select * from billcounter where dateTime >=date('now','-1 month') """
        c.execute(sql)
        rows = c.fetchall()
        sale = 0
        pending=0
        for row in rows:
            sale += row[6]
            pending += row[8]
            # print(row[3])
        conn.commit()
        print(sale)
        return (pending,sale, rows)
    except Error as e:
        print("error", e)

def get_pending_amount(mobile_no):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "select * from billcounter where mobile_no='"+mobile_no+"'"
        c.execute(sql)
        rows = c.fetchall()
        pending=0
        for row in rows:
            pending += row[8]
            # print(row[3])
        conn.commit()
        print("total pending amount",pending)
        return pending
    except Error as e:
        print("error", e)

def get_credit_amount(mobile_no):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    print("get prev credit")
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "select * from billcounter where mobile_no='"+mobile_no+"'"
        c.execute(sql)
        rows = c.fetchall()
        credit=0
        for row in rows:
            credit += row[11]
            # print(row[3])
        conn.commit()
        print("total pending amount",credit)
        return credit
    except Error as e:
        print("error", e)


def clear_prev_credit():
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "update billcounter set credit_amount ='0' where id;"
        c.execute(sql)
        rows = c.fetchall()
        conn.commit()
        return 0
    except Error as e:
        print("error", e)


def adjust_pendings(mobile_no,credit_amount):
    """
    Create a new billcounter
    :param conn:
    :param task:
    :return:
    """
    print("adjust pendings ")
    try:
        conn = sqlite3.connect('SQLite_Python.db')
        c = conn.cursor()
        sql = "select pending_amount,id from billcounter where mobile_no='"+mobile_no+"' and pending_amount > 0"
        c.execute(sql)
        rows = c.fetchall()
        print("pwnding rows",rows)
        pending=0
        for row in rows:
            if(credit_amount>0):
                # row[0] pending
                pending=row[0]-credit_amount
                if(pending<0):
                    credit_amount=abs(pending)
                    sql = "Update billcounter set pending_amount='0' where id=" + str(row[1]) + ";"
                    print("pending amount is ",pending," credit_amount ",credit_amount," billid ",row[1])
                    c.execute(sql)
                else:
                    credit_amount=0
                    print(" pending>0 amount is ", pending, " credit_amount ", credit_amount, " billid ", row[1])
                    sql = "Update billcounter set pending_amount='"+str(pending)+"'where id=" +str(row[1])+ ";"
                    c.execute(sql)
        conn.commit()
        print("total pending amount",pending)
        return credit_amount
    except Error as e:
        print("error", e)


# #
# insert into products( product_name, product_gauge, product_weight, product_quantity, product_purchase_price, product_sale_price)
# values ('metalsheet_guage_7',0, 1,100,5000,5000),
#        ('metalsheet_guage_1',0,1,100,6000,6500),
#        ('metal_rod',1,1,100,2000,2500),
#        ('coil',0.04,0.2,100,1000,1200),
#        ('stylesheet',0.2,2,100,7000,7100);

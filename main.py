from tkinter import *
from tkinter import ttk
from fpdf import FPDF
import models
from tksheet import Sheet
from models import *
import sys

product1 = "metalsheet_guage_7",
product1_weight = 1,
product1_quantity = 100,
product1_purchase_price = 5000,
product1_sale_price = 5000,

product2 = "metalsheet_guage_1",
product2_weight = 1,
product2_quantity = 100,
product2_purchase_price = 6000,
product2_sale_price = 6500

product3 = 'metalrod',
product3_gauge = 1,
product3_weight = 1,
product3_quantity = 100,
product3_purchase_price = 2000,
product3_sale_price = 2500

product4 = "coil"
product4_gauge = 0.04
product4_weight = 0.2
product4_quantity = 100
product4_purchase_price = 1000
product4_sale_price = 1200

product5 = "stylesheet"
product5_gauge = 0.2
product5_weight = 2
product5_quantity = 100
product5_purchase_price = 7000
product5_sale_price = 7100


def getPrice(combo_category):
    products_options = list()
    rows = models.get_stocks()
    for row in rows:
        print(row[0], combo_category)
        if (str(row[0]) == combo_category):

            return int(row[6])
    return 0


class bill_app:
    products_options = list()
    rows = models.get_stocks()

    for row in rows:
        products_options.append(str(row[0]) + " : " + row[1])

    subtotal = 0;

    def get_discount(self):
        discount_amount = self.discount.get()
        if discount_amount != "":
            discount_amount = int(discount_amount)
            self.discount_amount = discount_amount / 100 * self.subtotal

        else:
            self.discount_amount = 0
        self.txt_total = self.subtotal - self.discount_amount
        self.lbl_total.config(text="Total :" + str(self.txt_total))
        # txt_tax = self.txt_tax.get()
        # txt_total = self.txt_total.get()
        print("discount ", discount_amount)

    def saverecord(self):
        """ handle button click event and output text from entry area"""
        if(len(self.cart)==0):
            messagebox.showerror("Please Add Item","Please Add Item")
            return
        # date
        date_time = datetime.date.today()
        # customer
        custName = self.txtcustname.get()
        entry_mob = self.entry_mob.get()
        txtemail = self.txtemail.get()

        # bill counter
        discount_amount = self.discount.get()
        if discount_amount == "":
            self.txt_total = self.subtotal - self.discount_amount

        if self.txtpaid.get() != "":
            paid = int(self.txtpaid.get())
        else:
            paid = 0

        pending_amount = self.txt_total - paid
        credit_amount = 0
        remaining_amount=0
        if paid - self.txt_total < 0:
            prev_credit = models.get_credit_amount(entry_mob)
            print("prev",prev_credit)
            if (prev_credit > 0):
                remaining_amount = self.txt_total - abs((paid+int(prev_credit)) )
                print(prev_credit, remaining_amount)
                if (remaining_amount > 0):
                    pending_amount=abs(remaining_amount)
                    models.clear_prev_credit()
                    print("add to pending ",pending_amount)
                else:
                    credit_amount=abs(remaining_amount)
                    pending_amount=0
                    models.clear_prev_credit()
                    print("add to credit")
                # models.adjust_credit(entry_mob,)
        # shopkeeper
        return_amt = self.txtreturn.get()
        if (return_amt == ""):
            return_amt = 0
        # total return is

        if (pending_amount < 0 ):
            pending_amount = 0
            credit_amount = self.return_amount - int(return_amt)

        print("credit amount", credit_amount)

        if(credit_amount>0):
            # then adjust with previous pendings
           credit_amount= models.adjust_pendings(entry_mob,credit_amount)

        # pending_amount=pending_amount+models.get_pending_amount(entry_mob)
        products = ""
        for product in self.cart:
            temp = (product[0][1], product[1])
            products = products + product[0][1] + " * " + product[1] + " , "
            print("temp product", temp)
            product_id = models.modify_product(temp)

        print(custName, entry_mob, txtemail, self.txt_total, self.subtotal, products)

        self.reciept += "Customer Name   ======== " + custName + "\n"
        self.reciept += "Discount                ======== " + str(self.discount_amount) + "\n"
        self.reciept += "Subtotal              ======== " + str(self.subtotal) + "\n"
        self.reciept += "Total                  ======== " + str(self.txt_total) + "\n"
        self.reciept += "Total Paid             ======== " + str(paid) + "\n"
        self.reciept += "Return Amount          ======== " + str(return_amt) + "\n"
        self.reciept += "Credited Amount       ======== " + str(credit_amount+models.get_credit_amount(entry_mob)) + "\n"
        self.reciept += "PENDING AMOUNT         ======== " + str(pending_amount+models.get_pending_amount(entry_mob)) + "\n"
        print(self.reciept)
        self.textarea.delete(1.0, "end")
        self.textarea.insert(1.0, self.reciept)
        # mobile_no
        # customer_name
        # email
        # sub_total
        # total
        # discount
        # pending_amount
        # dateTime
        invoice = (
            entry_mob, custName, txtemail, products, self.subtotal, self.txt_total, self.discount_amount,
            pending_amount,paid,return_amt,credit_amount, date_time)
        bill_rowId = models.add_billcounter(invoice)
        self.bill_id = bill_rowId
        self.clear()

    def clean_name(self, name):
        return name.split(":")[1].strip()

    def clean_id(self, name):
        return name.split(":")[0].strip()

    #     add to cart function
    def add_to_cart(self):
        #     get the selected product
        #     add price to total amount
        # make list so that can be saved with cutomers table
        # product info
        combo_category = self.combo_category.get()
        comboQuantity = self.comboQuantity.get()
        if(combo_category=="" or comboQuantity==""):
            messagebox.showerror("No Product is Selected" , "No Product is selected")
            return
        # combosubcategory is the quantity of products
        item_price = getPrice(self.clean_id(combo_category))


        stock = models.get_product_quantity(self.clean_id(combo_category))
        if (int(stock) >= int(comboQuantity)):
            self.reciept += "Item            :" + combo_category + " * " + str(comboQuantity) + " *" + str(
                item_price) + "=" + str(int(comboQuantity) * item_price) + "\n"
            self.textarea.delete(1.0, "end")
            self.textarea.insert(1.0, self.reciept)
            self.subtotal += int(comboQuantity) * item_price
            product = (models.get_product(self.clean_id(combo_category)), comboQuantity)
            self.lbl_total.config(text="Total :" + str(self.subtotal))
            print(product)
            self.cart.append(product)
            print(self.cart)
            # self.bill_id=-1
            self.pending_amount = models.get_pending_amount(self.entry_mob.get())

            self.lbl_pending_amount.config(text="Pending :" + str(self.pending_amount))
            prev_credit = models.get_credit_amount(self.entry_mob.get())
            self.lbl_credit_amount.config(text="Credit  :" + str(prev_credit))
        else:
            messagebox.showinfo("Not enought stock", "Available stock is " + str(stock))

    def add_pending_amount(self, id):
        amount = int(self.pending_amount.get())
        models.update_pending_amount(id, amount)


    def add_pending(self, event=NONE):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        newWindow = Toplevel(self.root)
        newWindow.geometry('400x400')
        name = Label(newWindow, text="Pending amount")
        self.pending_amount = ttk.Entry(newWindow, text="Amount ")
        name.pack()
        self.pending_amount.pack()

        add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                         cursor="hand2", text="Add Pending ", command=lambda: self.add_pending_amount(row_data[0]))
        add_btn.pack()

    def adjust_credit_amount(self, id):
        amount = int(self.credit_amount.get())
        models.update_credit_amount(id, amount)

    def adjust_credit(self):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        newWindow = Toplevel(self.root)
        newWindow.geometry('400x400')
        name = Label(newWindow, text="Pending amount")
        self.credit_amount = ttk.Entry(newWindow, text="Amount ")
        name.pack()
        self.credit_amount.pack()

        add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                         cursor="hand2", text="Add Pending ", command=lambda: self.adjust_credit_amount(row_data[0]))
        add_btn.pack()


    def print_record_bill(self, event=NONE):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        self.print_bill(row_data[0])

    def view_bills(self, rows, sale=0, pending=0):
        if (len(rows) == 0):
            rows = models.get_bills()
        newWindow = Toplevel(self.root)
        newWindow.geometry('1400x700')
        info = Label(newWindow, text="Total Sale :" + str(sale) + ", Total pending:" + str(pending));
        info.grid(row="0", column="0")
        self.sheet = Sheet(newWindow, height=600, width=1400)
        self.sheet.enable_bindings(("single",
                                    "drag_select",
                                    "column_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "row_width_resize",
                                    "copy",
                                    "rc_insert_column",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_insert_row"))
        self.sheet.popup_menu_add_command("add pending amount", self.add_pending)
        self.sheet.popup_menu_add_command("adjust credit", self.adjust_credit)
        self.sheet.popup_menu_add_command("print bill", self.print_record_bill)
        self.sheet.grid(row=2, column=0, sticky="nswe")
        self.headers = ("id",
                        ' mobile no',
                        ' customer name',
                        ' email',
                        'products*quantity',
                        ' sub_total',
                        ' total',
                        ' discount',
                        ' pending amount',
                        'paid',
                        'return amount',
                        'credit amount',
                        'date'
                        )
        self.sheet.headers(self.headers)
        self.data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(len(rows))]
        self.sheet.data_reference(self.data)
        j: int = 0
        for row in rows:
            # i= len(a)
            r = j
            # print(r, j)
            self.sheet.set_row_data(r, values=row)
            j += 1

    def showDaily(self):
        bills = models.get_daily_profit()
        self.lbldaily.config(text=bills[1])
        self.view_bills(bills[2], bills[1], bills[0])
        print("show Daily", bills)

    def showMonthly(self):
        bills = models.get_monthly_profit()
        self.view_bills(bills[2], bills[1], bills[0])
        self.lblmonthly.config(text=bills[1])
        print("show Daily", bills)

    # employees
    def update_employee(self, row=[]):
        name = self.name_emp.get()
        print(name)
        data = (row[0],
                self.name_emp.get(),
                self.txtphone.get(),
                self.txtcnic.get(),
                self.txtaddress.get(),
                self.txtsalary.get(),
                self.txtloan.get())
        print(data)
        models.update_employee(data)
        print("added")

    def add_employee(self):
        name = self.name_emp.get()
        print(name)
        data = (self.name_emp.get(),
                self.txtphone.get(),
                self.txtcnic.get(),
                self.txtaddress.get(),
                self.txtsalary.get(),
                self.txtloan.get())
        print(data)
        models.add_employee(data)
        print("added")

    def openNewWindow(self, row=[]):
        newWindow = Toplevel(self.root)
        newWindow.geometry('400x400')
        name = Label(newWindow, text="Employee Name")
        self.name_emp = ttk.Entry(newWindow, text="Name ")

        lblphone = Label(newWindow, text="Phone no:")
        self.txtphone = ttk.Entry(newWindow, text="phone no:")

        lblcnic = Label(newWindow, text="CNIC")
        self.txtcnic = ttk.Entry(newWindow, text="CNIC")

        lbladdress = Label(newWindow, text="Address")
        self.txtaddress = ttk.Entry(newWindow, text="Address")
        lblsalary = Label(newWindow, text="Salary")
        self.txtsalary = ttk.Entry(newWindow, text="Salary")
        lblloan = Label(newWindow, text="Loan")
        self.txtloan = ttk.Entry(newWindow, text="Loan")
        name.pack()
        self.name_emp.pack()
        lblphone.pack()
        self.txtphone.pack()
        lblcnic.pack()
        self.txtcnic.pack()
        lbladdress.pack()
        self.txtaddress.pack()
        lblsalary.pack()
        self.txtsalary.pack()
        lblloan.pack()
        self.txtloan.pack()
        if (len(row) > 1):
            add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                             cursor="hand2", text="update Employee", command=lambda: self.update_employee(row))
            add_btn.pack()
        else:
            add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                             cursor="hand2", text="Add Employee", command=self.add_employee)
            add_btn.pack()
        print("opne new  ")

        print("edit stock")

    def edit_employee(self, event=None):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        self.openNewWindow(row_data)
        print(row_data)

    def delete_employee(self, event=None):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        models.delete_employee(row_data)
        print(row_data)

    def view_employees(self):
        rows = models.get_employees()
        newWindow = Toplevel(self.root)
        newWindow.geometry('900x400')
        self.btn_emp_add = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white",
                                  width=10, cursor="hand2", text="Add Employees", command=self.openNewWindow)
        self.btn_emp_add.grid(row="0", column="0")
        self.sheet = Sheet(newWindow, height=500, width=900)
        self.sheet.enable_bindings(("single",
                                    "drag_select",
                                    "column_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "row_width_resize",
                                    "copy",
                                    "rc_insert_column",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_insert_row"))
        self.sheet.popup_menu_add_command("Edit Employees", self.edit_employee)
        self.sheet.popup_menu_add_command("Delete Employees", self.delete_employee)

        self.sheet.grid(row=2, column=0, sticky="nswe")
        self.headers = ("id",
                        'Name',
                        'Phone No:',
                        'CNIC',
                        'Address',
                        'salary',
                        'loan')
        self.sheet.headers(self.headers)
        self.data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(len(rows))]
        self.sheet.data_reference(self.data)
        j: int = 0
        for row in rows:
            # i= len(a)
            r = j
            # print(r, j)
            self.sheet.set_row_data(r, values=row)
            j += 1

    # End Employees

    # stock
    def save_stock(self):
        row = (self.product_name.get(),
               self.product_gauge.get(),
               self.product_weight.get(),
               self.product_quantity.get(),
               self.product_purchase_price.get(),
               self.product_sale_price.get())
        models.add_product(row)
        print("save stock")

    def update_stock(self, row):
        row2 = (row[0],
                self.product_name.get(),
                self.product_gauge.get(),
                self.product_weight.get(),
                self.product_quantity.get(),
                self.product_purchase_price.get(),
                self.product_sale_price.get())
        print("row2", row2)
        models.update_product(row2)
        print("add stock", row)

    def edit_stock(self, row=[]):
        # self.product_name_txt_var = ""
        # self.product_gauge_txt_var = ""
        # self.product_weight_txt_var = ""
        # self.product_quantity_txt_var = ""
        # self.product_purchase_price_txt_var =""
        # self.product_sale_price_txt_var = ""

        # if (len(row) > 1):
        #     self.product_name_txt_var = row[1]
        #     self.product_gauge_txt_var = row[2]
        #     self.product_weight_txt_var = row[3]
        #     self.product_quantity_txt_var = row[4]
        #     self.product_purchase_price_txt_var = row[5]
        #     self.product_sale_price_txt_var = row[6]

        newWindow = Toplevel(self.root)
        newWindow.geometry('400x400')
        name = Label(newWindow, text="Product Name")

        self.product_name = ttk.Entry(newWindow, text="Product Name")
        # ,textvariable=self.product_name_txt_var)
        gauge = Label(newWindow, text="Gauge")
        self.product_gauge = ttk.Entry(newWindow, text="Product Gauge:")
        # ,textvariable=  self.product_gauge_txt_var )

        # ,textvariable=self.product_weight_txt_var)
        product_weight = Label(newWindow, text="Weight")
        self.product_weight = ttk.Entry(newWindow, text="weight")

        quantity = Label(newWindow, text="Quantity")
        self.product_quantity = ttk.Entry(newWindow, text="Quantity")
        # ,textvariable=self.product_quantity_txt_var)
        product_purchase_price = Label(newWindow, text="purchase price")
        self.product_purchase_price = ttk.Entry(newWindow, text="purchase price")
        # ,textvariable=self.product_purchase_price_txt_var)
        salePrice = Label(newWindow, text="sale_price")
        self.product_sale_price = ttk.Entry(newWindow, text="product_sale_price")
        # ,textvariable=self.product_sale_price_txt_var)
        name.pack()
        self.product_name.pack()
        gauge.pack()
        self.product_gauge.pack()
        product_weight.pack()
        self.product_weight.pack()
        quantity.pack()
        self.product_quantity.pack()
        product_purchase_price.pack()
        self.product_purchase_price.pack()
        salePrice.pack()
        self.product_sale_price.pack()

        if (len(row) < 1):

            add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                             cursor="hand2", text="Add Product", command=self.save_stock)
            add_btn.pack()
        else:
            add_btn = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white", width=10,
                             cursor="hand2", text="update Product", command=lambda: self.update_stock(row))
            add_btn.pack()
        print("opne new  ")

    def edit_product(self, event=None):
        last_selected = self.sheet.get_currently_selected(get_coords=False, return_nones_if_not=False)
        print(last_selected)
        # if len(last_selected) > 1 and last_selected[0] == "row":
        row_data = self.sheet.get_row_data(last_selected[0])
        self.edit_stock(row_data)
        print(row_data)

    def showStocks(self):
        rows = models.get_stocks()
        newWindow = Toplevel(self.root)
        newWindow.geometry('900x400')
        self.btn_stock_add = Button(newWindow, font=('times new roman', 10, 'bold'), bg="orangered", fg="white",
                                    width=10, cursor="hand2", text="Add Product", command=self.edit_stock)
        self.btn_stock_add.grid(row="0", column="0")
        self.sheet = Sheet(newWindow, height=500, width=900)
        self.sheet.enable_bindings(("single",
                                    "drag_select",
                                    "column_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "row_width_resize",
                                    "copy",
                                    "rc_insert_column",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_insert_row"))
        self.sheet.popup_menu_add_command("Edit Stock", self.edit_product)

        self.sheet.grid(row=2, column=0, sticky="nswe")
        self.headers = ("id",
                        ' product Name',
                        ' product Gauge',
                         'product Weight',
                        ' product Quantity',
                        ' product Purchase price',
                        ' product Sale price')
        self.sheet.headers(self.headers)
        self.data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(len(rows))]
        self.sheet.data_reference(self.data)
        j: int = 0
        for row in rows:
            # i= len(a)
            r = j
            # print(r, j)
            self.sheet.set_row_data(r, values=row)
            j += 1
        # stock_str = "Products Stocks \n\n"
        # for row in rows:
        #     stock_str+=str(row[1]) +"----------" +str(row[4]) +"\n"
        # self.stocktxt.insert(1.0,stock_str)

    def search_bill_by_phone(self):
        # self.txt_entry_search
        phone=self.txt_phone_search.get()
        rows = models.get_bills_by_phone(phone)
        self.search_bills(rows)


    def search_bill_by_date(self):
        date = self.txt_entry_search.get()
        rows = models.get_bills_by_date(date)
        self.search_bills(rows)

    # end Stock
    def search_bills(self,rows):
        newWindow = Toplevel(self.root)
        newWindow.geometry('1400x700')
        # info = Label(newWindow, text="Total Sale :" + str(sale) + ", Total pending:" + str(pending));
        # info.grid(row="0", column="0")

        self.sheet = Sheet(newWindow, height=600, width=1400)
        self.sheet.enable_bindings(("single",
                                    "drag_select",
                                    "column_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "row_width_resize",
                                    "copy",
                                    "rc_insert_column",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_insert_row"))
        self.sheet.popup_menu_add_command("add pending amount", self.add_pending)
        self.sheet.grid(row=2, column=0, sticky="nswe")

        self.headers = ("id",
                        ' Mobile No',
                        ' Customer name',
                        ' email',
                        ' products*quantity',
                        ' Sub total',
                        ' Total',
                        ' discount',
                        ' Pending amount',
                        'paid',
                        'return amount',
                        'credit amount',
                        ' Date'
                        )
        self.sheet.headers(self.headers)
        self.data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(len(rows))]
        self.sheet.data_reference(self.data)
        j: int = 0
        for row in rows:
            # i= len(a)
            r = j
            # print(r, j)
            self.sheet.set_row_data(r, values=row)
            j += 1

    def print_bill(self, id):
        row = models.get_bill_by_id(id);
        if(len(row)==0):
            messagebox.showerror("Please save bill first","Please save bill first")
            return

        reciept = "                 RECIEPT                      \n"
        products = row[4].split(',')
        products.pop()
        for product in products:
            reciept += "Item            :" + product +'\n'

        print(row, products)
        reciept += "Customer Name           ======== " +         str(row[2]) + "\n"
        reciept += "Discount                ======== " + str(row[7]) + "\n"
        reciept += "Subtotal                ======== " +   str(row[5]) + "\n"
        reciept += "Total                   ======== " +  str(row[6]) + "\n"
        reciept += "Total Paid              ======== " +  str(row[9]) + "\n"
        reciept += "Retunr Amount           ======== " +  str(row[10]) + "\n"
        reciept += "Credited Amount         ======== " +   str(row[11]) + "\n"
        reciept += "PENDING AMOUNT          ======== " +  str(row[8]) + "\n"
        print("2nd ",reciept)
        self.printBill(reciept)

    def printBill(self,reciept):
             pdf = FPDF(format='letter')
             # Add a page
             pdf.add_page()
             # set style and size of font
             # that you want in the pdf
             pdf.set_font("Arial", size=10)
             lines=self.reciept.strip('\n')
             print("lines",lines)
             # create a cell
             j=1
             for i in reciept.splitlines():
                 print(i)
                 pdf.cell(150, 7, txt=i, ln=j, align="L")
                 j=j+1
             # # add another cell
             # clear reciept
             # save the pdf with name .pdf
             pdf.output(str(self.bill_id)+".pdf")
             self.bill_id=-1

        # view Customers

    def view_customers(self):
        rows = models.get_customers()
        newWindow = Toplevel(self.root)
        newWindow.geometry('800x500')
        # info = Label(newWindow, text="Total Sale :" + str(sale) + ", Total pending:" + str(pending));
        # info.grid(row="0", column="0")

        self.sheet = Sheet(newWindow, height=400, width=900)
        self.sheet.enable_bindings(("single",
                                    "drag_select",
                                    "column_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "arrowkeys",
                                    "column_width_resize",
                                    "row_width_resize",
                                    "copy",
                                    "rc_insert_column",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_insert_row"))
        self.sheet.popup_menu_add_command("add pending amount", self.add_pending)
        self.sheet.grid(row=2, column=0, sticky="nswe")

        self.headers = (
            ' Customer Name',
            ' Phone No:',
            ' Total',
            ' Pending',
            ' Total Paid',
            ' Credit'
        )
        self.sheet.headers(self.headers)
        self.data = [[f"Row {r} Column {c}" for c in range(3)] for r in range(len(rows))]
        self.sheet.data_reference(self.data)
        j: int = 0
        for row in rows:
            # i= len(a)
            r = j
            # print(r, j)
            self.sheet.set_row_data(r, values=row)
            j += 1
        pass

    def calc_pay(self):
        pay = int(self.txtpaid.get())

        if (self.discount_amount != 0):
            self.return_amount = pay - self.txt_total
        else:
            self.return_amount = pay - self.subtotal
        print("return amount is ", self.return_amount)
        self.lbl_return_amount.config(text="return :" + str(self.return_amount))




    def clear(self):
        self.pending_amount=0
        self.discount_amount = 0
        self.subtotal = 0
        self.txt_total = 0
        self.cart = list()
        self.lbl_total.config(text="Total")
        self.lbl_pending_amount.config(text="Pending :")
        self.lbl_return_amount.config(text="Return  :")
        self.lbl_credit_amount.config(text="Credit :")

        self.reciept = "                 RECIEPT                      \n"
        self.txtpaid.delete(0, END)
        self.entry_mob.delete(0, END)
        self.txtcustname.delete(0, END)
        self.txtemail.delete(0, END)
        self.comboQuantity.delete(0, END)
        self.discount.delete(0, END)

    def __init__(self, root):
        self.return_amount = 0
        self.pending_amount=0
        self.discount_amount = 0
        self.txt_total = 0
        self.bill_id = -1
        self.cart = list()
        self.reciept = "                 RECIEPT                      \n"
        self.root = root
        self.root.geometry("1530x800+0+0")
        self.root.title("Billing Software")

        lbl_title = Label(self.root, text="AL HAFIZ", font=(
            "times new roman", 35, "bold"), bg="white", fg="black")
        lbl_title.place(x=0, y=0, width=1360, height=45)

        main_Frame = Frame(self.root, bd=5, relief=GROOVE, bg="white")
        main_Frame.place(x=0, y=45, width=1360, height=650)

        # custumer farme
        cust_Frame = LabelFrame(main_Frame, text="Customer", font=("times new roman", 12, "bold"), bg="white",
                                fg="black")
        cust_Frame.place(x=10, y=5, width=350, height=150)

        self.lbl_mob = Label(cust_Frame, text="Mobile No", font=(
            "times new roman", 12, "bold"), bg="white", fg="black")
        self.lbl_mob.grid(row=0, column=0, stick=W, padx=5, pady=2)

        self.entry_mob = ttk.Entry(cust_Frame, font=(
            "times new roman", 10, "bold"), width=24)
        self.entry_mob.grid(row=0, column=1)

        self.lblcustname = Label(cust_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Customer Name",
                                 bd=4)
        self.lblcustname.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.txtcustname = ttk.Entry(cust_Frame, font=(
            'times new roman', 10, 'bold'), width=24)
        self.txtcustname.grid(row=1, column=1, sticky=W, padx=5, pady=2)

        self.lblemail = Label(cust_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="Email", bd=4)
        self.lblemail.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        self.txtemail = ttk.Entry(cust_Frame, font=(
            'times new roman', 10, 'bold'), width=24)
        self.txtemail.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        # self.lbldiscount = Label(cust_Frame, font=(
        #     'times new roman', 12, 'bold'), bg="white", text="Discount", bd=4)
        # self.lbldiscount.grid(row=3, column=0, sticky=W, padx=5, pady=2)
        #
        # self.txtdiscount = ttk.Entry(cust_Frame, font=(
        #     'times new roman', 10, 'bold'), width=24)
        # self.txtdiscount.grid(row=3, column=1, sticky=W, padx=5, pady=2)

        # product frame
        product_Frame = LabelFrame(main_Frame, text="Product", font=("times new roman", 12, "bold"), bg="white",
                                   fg="black")
        product_Frame.place(x=370, y=5, width=620, height=140)

        # Stock
        stock_Frame = LabelFrame(main_Frame, text="Stock", font=("times new roman", 12, "bold"), bg="white",
                                 fg="black")
        stock_Frame.place(x=10, y=200, width=400, height=400)

        self.btnStock = Button(stock_Frame, height=1, text="View Stocks", font=('times new roman', 15, 'bold'),
                               bg="orangered", fg="white", width=10, cursor="hand2", command=self.showStocks)
        self.btnStock.grid(row=0, column=0)

        self.lbl_total = Label(stock_Frame, font=(
            'times new roman', 16, 'bold'), bg="white", text=" Total", bd=4)
        self.lbl_total.grid(row=3, column=0)

        self.lbl_return_amount = Label(stock_Frame, font=(
            'times new roman', 16, 'bold'), bg="white", text="Return :", bd=4)
        self.lbl_return_amount.grid(row=5, column=0)
        self.lbl_pending_amount= Label(stock_Frame, font=(
            'times new roman', 16, 'bold'), bg="white", text="Pending :", bd=4)
        self.lbl_pending_amount.grid(row=10, column=0)
        self.lbl_credit_amount= Label(stock_Frame, font=(
            'times new roman', 16, 'bold'), bg="white", text="Credit :", bd=4)
        self.lbl_credit_amount.grid(row=15, column=0)
        # self.stocktxt = Text(stock_Frame,  bg="white", fg="black",
        #                      font=("times new roman", 12, "bold"))
        # self.stocktxt.grid(row=2,column=0)

        # self.textarea.pack(fill=BOTH, expand=1)

        # category

        self.lblcategory = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Select Product",
                                 bd=4)

        self.lblcategory.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.combo_category = ttk.Combobox(product_Frame, font=('times new roman', 10, 'bold'), width=24,
                                           state="readonly")
        self.combo_category['values'] = self.products_options
        self.combo_category.grid(row=0, column=1, sticky=W, padx=5, pady=2)

        # subcategory
        self.lblQuantity = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Quantity",
                                 bd=4)
        self.lblQuantity.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.comboQuantity = ttk.Entry(product_Frame, font=('times new roman', 10, 'bold'),
                                       width=24)
        self.comboQuantity.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        #
        # # product name
        # self.lblproduct = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Product Name",
        #                         bd=4)
        # self.lblproduct.grid(row=2, column=0, sticky=W, padx=5, pady=2)
        #
        # self.comboproduct = ttk.Combobox(product_Frame, state="readonly", font=('times new roman', 10, 'bold'),
        #                                  width=24)
        # self.comboproduct.grid(row=2, column=1, sticky=W, padx=5, pady=2)
        #
        # # price
        #
        # self.lblprice = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Price", bd=4)
        # self.lblprice.grid(row=0, column=3, sticky=W, padx=5, pady=2)
        #
        # self.comboprice = ttk.Combobox(product_Frame, state="readonly", font=('times new roman', 10, 'bold'), width=24)
        # self.comboprice.grid(row=0, column=4, sticky=W, padx=5, pady=2)
        #
        # # qty
        #
        # self.lblqty = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Qty", bd=4)
        # self.lblqty.grid(row=1, column=3, sticky=W, padx=5, pady=2)
        #
        # self.comboqty = ttk.Entry(product_Frame, font=('times new roman', 10, 'bold'), width=26)
        # self.comboqty.grid(row=1, column=4, sticky=W, padx=5, pady=2)
        #
        # # weight
        #
        # self.lblweight = Label(product_Frame, font=('times new roman', 12, 'bold'), bg="white", text="Weight", bd=4)
        # self.lblweight.grid(row=2, column=3, sticky=W, padx=5, pady=2)
        #
        # self.comboweight = ttk.Entry(product_Frame, font=('times new roman', 10, 'bold'), width=26)
        # self.comboweight.grid(row=2, column=4, sticky=W, padx=5, pady=2)

        # rignt biling frame
        rightlabelframe = LabelFrame(main_Frame, text="BILL AREA", font=("times new roman", 12, "bold"), bg="white",
                                     fg="black")
        rightlabelframe.place(x=850, y=150, width=480, height=440)

        scroll_y = Scrollbar(rightlabelframe, orient=VERTICAL)
        self.textarea = Text(rightlabelframe, yscrollcommand=scroll_y.set, bg="white", fg="black",
                             font=("times new roman", 12, "bold"))
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH, expand=1)

        # TOTAL BILLL
        bottom_Frame = LabelFrame(main_Frame, text="Bill Counter", font=("times new roman", 12, "bold"), bg="white",
                                  fg="black")
        bottom_Frame.place(x=0, y=465, width=840, height=125)

        self.lbldiscount = Label(bottom_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="discount", bd=4)
        self.lbldiscount.grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.discountBtn = Button(bottom_Frame, height=1, text="discount", font=('times new roman', 10, 'bold'),
                                  bg="orangered", fg="white", cursor="hand2", command=self.get_discount)
        self.discountBtn.grid(row=0, column=1, sticky=W, padx=150, pady=2)

        self.discount = ttk.Entry(bottom_Frame, text="", font=(
            'times new roman', 10, 'bold'), width=20)
        self.discount.grid(row=0, column=1, sticky=W, padx=5, pady=2)

        self.lbl_paid = Label(bottom_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="Paid", bd=4)
        self.lbl_paid.grid(row=1, column=0, sticky=W, padx=5, pady=2)
        #
        self.txtpaid = ttk.Entry(bottom_Frame, font=(
            'times new roman', 10, 'bold'), width=20)
        self.txtpaid.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        # pay button
        self.payBtn = Button(bottom_Frame, height=1, text="pay", font=('times new roman', 10, 'bold'),
                             bg="orangered", fg="white", width="7", cursor="hand2", command=self.calc_pay)
        self.payBtn.grid(row=1, column=1, sticky=W, padx=150, pady=2)
        # return text field
        self.lbl_return = Label(bottom_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="Return", bd=4)
        self.lbl_return.grid(row=2, column=0, sticky=W, padx=5, pady=2)
        #
        self.txtreturn = ttk.Entry(bottom_Frame, font=(
            'times new roman', 10, 'bold'), width=26)
        self.txtreturn.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        #
        # self.txt_total = ttk.Entry(bottom_Frame, font=(
        #     'times new roman', 10, 'bold'), width=26)
        # self.txt_total.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        # Button frame
        btn_Frame = Frame(bottom_Frame, bd=2, bg="white")
        btn_Frame.place(x=320, y=0)

        self.btnaddtocart = Button(btn_Frame, height=2, text="Add to Cart", font=('times new roman', 12, 'bold'),
                                   bg="orangered", fg="white", cursor="hand2", command=self.add_to_cart)
        self.btnaddtocart.grid(row=0, column=0)

        self.btnsavebill = Button(btn_Frame, height=2, text="Save Bill", font=('times new roman', 12, 'bold'),
                                  bg="orangered", fg="white", cursor="hand2", command=self.saverecord)
        self.btnsavebill.grid(row=0, column=1)

        self.btnprint = Button(btn_Frame, height=2, text="Print", font=('times new roman', 12, 'bold'),
                               bg="orangered", fg="white", cursor="hand2", command=lambda:self.print_bill(self.bill_id))
        self.btnprint.grid(row=0, column=2)

        self.btnview = Button(btn_Frame, height=2, text="View Bills", font=('times new roman', 12, 'bold'),
                              bg="orangered", fg="white", cursor="hand2", command=lambda: self.view_bills([]))
        self.btnview.grid(row=0, column=3)
        self.btncustomers = Button(btn_Frame, height=2, text="Customers", font=('times new roman', 12, 'bold'),
                                   bg="orangered", fg="white", cursor="hand2", command=self.view_customers)
        self.btncustomers.grid(row=0, column=4)
        self.btnexit = Button(btn_Frame, height=2, text="EXIT", font=('times new roman', 12, 'bold'),
                              bg="orangered", fg="white", width=3, cursor="hand2" ,command=lambda: sys.exit(0))
        self.btnexit.grid(row=0, column=5)

        # EXPENCE FRAME
        exp_Frame = LabelFrame(main_Frame, text="Expence", font=("times new roman", 12, "bold"), bg="white",
                               fg="black")
        exp_Frame.place(x=1000, y=0, width=375, height=135)

        self.btndaily = Button(exp_Frame, height=1, text="Daily Expense", font=('times new roman', 15, 'bold'),
                               bg="orangered", fg="white", width=15, cursor="hand2", command=self.showDaily)
        self.btndaily.grid(row=0, column=0)
        self.lbldaily = Label(exp_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="-----", bd=4)
        self.lbldaily.grid(row=0, column=1)

        self.btnmonthly = Button(exp_Frame, height=1, text="Monthly Expense", font=('times new roman', 15, 'bold'),
                                 bg="orangered", fg="white", width=15, cursor="hand2", command=self.showMonthly)
        self.btnmonthly.grid(row=3, column=0)
        self.lblmonthly = Label(exp_Frame, font=(
            'times new roman', 12, 'bold'), bg="white", text="-----", bd=4)
        self.lblmonthly.grid(row=3, column=1)
        self.btnEmployees = Button(exp_Frame, height=1, text="Employees", font=('times new roman', 15, 'bold'),
                                   bg="orangered", fg="white", width=15, cursor="hand2", command=self.view_employees)
        self.btnEmployees.grid(row=4, column=0)

        # Search area

        search_Frame = Frame(main_Frame, bd=2, bg="white")
        search_Frame.place(x=350, y=155, width=500, height=40)

        self.lblbill = Label(search_Frame, font=('times new roman', 12, 'bold'), fg="white", bg="red",
                             text="DATE e.g(2021-09-25)")
        self.lblbill.grid(row=0, column=0, sticky=W, padx=1)

        self.txt_entry_search = ttk.Entry(search_Frame, font=(
            'times new roman', 10, 'bold'), width=24)
        self.txt_entry_search.grid(row=0, column=1, sticky=W, padx=2)

        self.btnsearch = Button(search_Frame, text="Search", font=('times new roman', 10, 'bold'),
                                bg="orangered", fg="white", width=6, cursor="hand2", command=self.search_bill_by_date)
        self.btnsearch.grid(row=0, column=2)

        search_Frame2 = Frame(main_Frame, bd=2, bg="white")
        search_Frame2.place(x=350, y=180, width=500, height=40)

        self.lblbill = Label(search_Frame2, font=('times new roman', 12, 'bold'), fg="white", bg="red",
                             text="Phone no                     :")
        self.lblbill.grid(row=0, column=0, sticky=W, padx=1)

        self.txt_phone_search = ttk.Entry(search_Frame2, font=(
            'times new roman', 10, 'bold'), width=24)
        self.txt_phone_search.grid(row=0, column=1, sticky=W, padx=2)

        self.btnsearch2 = Button(search_Frame2, text="Search", font=('times new roman', 10, 'bold'),
                                bg="orangered", fg="white", width=6, cursor="hand2", command=self.search_bill_by_phone)
        self.btnsearch2.grid(row=0, column=2)


if __name__ == '__main__':
    root = Tk()
    obj = bill_app(root)
    root.mainloop()

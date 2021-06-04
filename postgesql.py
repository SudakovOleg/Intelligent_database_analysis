import psycopg2
import numpy as np
from kahonen import KahononNetwork
from prettytable import PrettyTable
from perseptron import Perception

conn = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="admin", 
  host="127.0.0.1", 
  port="5432"
)

print("Database opened successfully")

while True:
    #------Function space---------
    def space():
        print("\n\n")
    #------Function space---------
    
    #------Function print_menu---------
    def print_menu():
        space()
        print("------    Menu    ------")
        print("1) View all products")
        print("2) Add new product")
        print("3) Update product")
        print("4) Delete product")
        print("5) Conduct training for the Kohonen network")
        print("6) Conduct deep learning")
        print("7) Check the data for validity")
        print("8) Exit")
        print("------------------------")
        space()
        return int(input("You'r choice?: "))
    #------Function print_menu---------
    
    #------Function print_table---------
    def print_table(headers, data):
        cols = len(headers)
        table = PrettyTable(headers)
        for row in data:
            table.add_row(row[:cols])
        print(table)
    #------Function print_table---------
    
    #------Function view_all---------
    def view_all():
        cur = conn.cursor()
        cur.execute("SELECT id, productname, manufacturer, productcount, price FROM products")
        rows = cur.fetchall()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name='products';")
        columns = cur.fetchall()
        print_table(columns,rows)
        return rows
    #------Function view_all---------
    
    #------Function add_product---------
    def add_product(productname, manufacturer, productcount, price):
        cur = conn.cursor()
        excute_str = str("INSERT INTO products (productname, manufacturer, productcount, price) " +
                     "VALUES ('" + productname + "', " 
                            "'" + manufacturer + "', "
                                + productcount + ", "
                                + price + ")")
        cur.execute(excute_str)
        conn.commit()
        print("Records inserted successfully")
        view_all()
    #------Function add_product---------                
    
    #------Function update_product--------- 
    def update_product(req_id):
        cur = conn.cursor()
        while True:
            view_all()
            field = input("What field would you like to edit? (use 0 for exit)")
            if field == "0":
                break
            value = input("Please, enter the new value: ")
            if field == "0":
                break
            excute_str = str("UPDATE products set '" + field + "'='" + value + "' WHERE id=" + req_id)
            cur.execute(excute_str)
            conn.commit()
    #------Function update_product--------- 
    
    #------Function delete_product--------- 
    def delete_product(req_id):
        cur = conn.cursor()
        excute_str = str("DELETE FROM products WHERE id=" + req_id)
        cur.execute(excute_str)
        conn.commit()
    #------Function delete_product--------- 
    
    answer = print_menu()
    space()
    
    if answer == 1:
        print("View all products")
        rows = view_all()
    elif answer == 2:
        print("Add new product")
        add_product(input("Please, endter productname: "),
                    input("Please, enter manufacturer: "),
                    input("Please, enter productcount: "),
                    input("Please, enter price: "))
    elif answer == 3:
        print("Update product")
        view_all()
        update_product(input("What would you like to update? (id): "))
    elif answer == 4:
        print("Delete product")
        delete_product(input("What would you like to delete? (id): "))
    elif answer == 5:
        cur = conn.cursor()
        cur.execute("SELECT productname, manufacturer, price FROM products")
        rows = cur.fetchall()
        net = KahononNetwork(3)
        print("Output before ", net.output_n)
        data = net.train_auto_output(net.normalization(rows))
        print("Output after ", net.output_n)
        for out in range(net.output_n):
            print("\n____CLUSTER  ", out, "____")
            for i in range(len(rows)):
                if int(data[i][-1]) == out:
                    print(rows[i])
            print("____________________")
    elif answer == 6:
        cur = conn.cursor()
        cur.execute("SELECT productname, manufacturer, price FROM public.products")
        rows = cur.fetchall()
        net = KahononNetwork(3)
        print("Output before ", net.output_n)
        data = net.normalization(rows)
        data = net.train_auto_output(data[:-1])
        print("Output after ", net.output_n)
        for out in range(net.output_n):
            print("\n____CLUSTER  ", out, "____")
            for i in range(len(rows) - 1):
                if int(data[i][-1]) == out:
                    print(rows[i])
            print("____________________")
        per = Perception(3, net.output_n,  net.output_n * 1.5, 1)
        train = []
        for vector in data:
            v = [0 for x in range(net.output_n)]
            v[int(vector[-1])] = 1
            print(v)
            train.append(v)
        v = [0 for x in range(net.output_n)]
        train.append(v)
        train_y = np.array([np.array(x) for x in train[:]])
        print(data, "x: ", data[0:-1,0:-1], "y: ", train[:-1])
        per.train(data[:-1,0:-1],train_y, 1000, 1)
        cur = conn.cursor()
        cur.execute("SELECT productname, manufacturer, price FROM public.products")
        rows = cur.fetchall()
        data = net.normalization(rows)
        print(data)
        per.predict(data, rows, train_y)
    elif answer == 7:
        True
    elif answer == 8:
        break
    else:
        print("What did you mean?")
import psycopg2
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from SOM import SOM
from kahonen import KahononNetwork
from prettytable import PrettyTable

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
        print("------   Menu    ------")
        print("1) View all products")
        print("2) Add new product")
        print("3) Update product")
        print("4) Delete product")
        print("5) Exit")
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
        cur.execute("SELECT productname, manufacturer, productcount, price FROM products")
        rows = cur.fetchall()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name='products';")
        columns = cur.fetchall()
        #print_table(columns,rows)
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
            excute_str = str("UPDATE products set " + field + "=" + value + "WHERE id=" + req_id)
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
        net = KahononNetwork(4)
        som_dim = 2
        data = np.array(net.normalization(rows), dtype=float)
        #Train a 20x30 SOM with 400 iterations
        som = SOM(2, 1, 3, 400)
        som.train(data)
        #Get output grid
        print(som.get_centroids())
        
    elif answer == 2:
        print("Add new product")
        add_product(input("Please, endter productname: "),
                    input("Please, enter manufacturer: "),
                    input("Please, enter productcount: "),
                    input("Please, enter price: "))
    elif answer == 3:
        print("Update product")
        update_product(input("What would you like to update? (id): "))
    elif answer == 4:
        print("Delete product")
        delete_product(input("What would you like to delete? (id): "))
    elif answer == 5:
        break
    else:
        print("What did you mean?")
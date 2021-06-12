'''
Argument parsing section. 
Accepts command-line arguments and handles the main errors associated with them. 
Only the module for working with arguments is enabled to speed up the program.
'''
import argparse

parser = argparse.ArgumentParser(prog='DBscan',
                                description='The program is designed to test an intelligent algorithm for scanning databases')
required_args = parser.add_argument_group('required arguments')
required_args.add_argument('-u','--user',dest='user',required=True,
                        help='This is the user name for logging in to the database management system')
required_args.add_argument('-p','--password',dest='password',required=True,
                        help='This is the user password for logging in to the database management system')
required_args.add_argument('-ip', '--host', dest='ip', required=True,
                        help='Data to connect to a host with a database')
parser.add_argument('-l', '--logging', dest='level', default="warning", 
                        help='Setup logging level')
args = parser.parse_args()

'''
Logging section. 
An additional module is connected, which is responsible for logging the program and other modules. 
It is configured before the program continues to work.
'''
import logging

level_config = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warning': logging.WARNING}
logging.basicConfig(format='%(levelname)s - %(message)s', level=level_config[args.level])

'''
The database connection section. 
Displays information at the debug level about the data used for the connection. 
Using a special module, it attempts to connect.
'''
import psycopg2

logging.debug("user = %s" % args.user)
logging.debug("password = %s" % "********")
logging.debug("ip = %s" % args.ip)

conn = psycopg2.connect(
  database="postgres", 
  user=args.user, 
  password=args.password, 
  host=args.ip, 
  port="5432"
)
print("Database opened successfully")

'''
The main part of the program. 
All necessary modules are loaded. The work starts with printing the menu. 
The program is executed cyclically until an exit signal is received.
'''
import numpy as np
from controller_ai import Ai
from prettytable import PrettyTable
from kahonen import KahononNetwork

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
        #Извлечение данных из БД
        cur = conn.cursor()
        cur.execute("SELECT productname, manufacturer FROM products")
        rows = cur.fetchall()
        #Обучение сети Кохонена, без персептрона
        net = KahononNetwork(3)
        print("Output before ", net.output_n)
        data = net.train_auto_output(net.normalization(rows))
        print("Output after ", net.output_n)
        #Проверка результата обучения
        for out in range(net.output_n):
            print("\n____CLUSTER  ", out, "____")
            for i in range(len(rows)):
                if int(data[i][-1]) == out:
                    print(rows[i])
            print("____________________")
    elif answer == 6:
        #Извлечение данных из БД
        cur = conn.cursor()
        cur.execute("SELECT productname, manufacturer FROM public.products")
        rows = cur.fetchall()
        #Обучение сетей на всех строках таблицы кроме последней
        ai = Ai(rows[:-1])
        #Предсказание на всех строках таблицы
        ai.predict(rows)
    elif answer == 7:
        True
    elif answer == 8:
        break
    else:
        print("What did you mean?")
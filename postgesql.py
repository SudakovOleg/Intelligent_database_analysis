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
from psycopg2 import Error

logging.debug("user = %s" % args.user)
logging.debug("password = %s" % "********")
logging.debug("ip = %s" % args.ip)

try:
    conn = psycopg2.connect(
      database="postgres", 
      user=args.user, 
      password=args.password, 
      host=args.ip, 
      port="5432"
    )
    print("Database opened successfully")
except (Exception, Error) as error:
    print("Error when working with PostgreSQL ", error)

'''
The main part of the program. 
All necessary modules are loaded. The work starts with printing the menu. 
The program is executed cyclically until an exit signal is received.
'''
import os
import numpy as np
from controller_ai import Ai
from prettytable import PrettyTable
from kahonen import KahononNetwork

while True:
    os.system('cls||clear')

    def print_menu():
        '''
        Menu print function. 
        In addition to printing, it handles exceptions for incorrect input.
        '''
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
        print("\n")
        
        try:
            answer = int(input("You'r choice?: "))
        except Exception:
            logging.debug("Answer = %s" % answer)
            answer = -1
        return answer
    
    def print_table(headers, data):
        '''
        Function for printing a table. 
        Accepts a list of headers and a list of data.
        '''
        logging.debug(headers)
        logging.debug(data)
        cols = len(headers)
        table = PrettyTable(headers)
        for row in data:
            table.add_row(row[:cols])
        print(table)
    
    def choose_table():
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');")
        tables = []
        for col in cur.fetchall():
            col = str(col)
            tables.append(col.replace('(', '').replace(')', '').replace(',', '').replace('\'', ''))
        logging.debug("Tables = %s" % tables)
        input_num = 1
        for table in tables:
            print(input_num, ") " + str(table) + ": ")
            input_num += 1
        try:
            answer = int(input("You'r choice?: "))
            return tables[answer - 1]
        except Exception:
            logging.debug("Answer = %s" % answer)
            return ""

    
    def view(table, columns="*"):
        '''
        String reading function. 
        Retrieves data from a database table. 
        '''
        logging.debug("Table = %s" % table)
        logging.debug("Columns = %s" % columns)
        cur = conn.cursor()
        cur.execute("SELECT " + ', '.join(columns) + "FROM " + table)
        rows = cur.fetchall()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name='" + table + "';")
        columns = cur.fetchall()
        logging.debug(rows)
        logging.debug("Columns = %s" % columns)
        print_table(columns,rows)
    
    def add(table):
        '''
        Function for adding rows to a table. 
        Accepts the table and the id to change.
        '''
        logging.debug("Table = %s" % table)
        cur = conn.cursor()
        cur.execute("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name='" + table + "';")
        columns = []
        for col in cur.fetchall():
            col = str(col)
            columns.append(col.replace('(', '').replace(')', '').replace(',', '').replace('\'', ''))
        logging.debug("Columns = %s" % columns)
        values_columns = []
        while True:
            input_num = 1
            print("Enter the number to add the item to the table " + table + ": ")
            for col in columns:
                print(input_num, ") ", col)
                input_num += 1
            print("\nOr enter the number to exclude from the append: ")
            for val in values_columns:
                print(input_num, ") ", val)
                input_num += 1
            print("\n0) Enter zero to exit\n")
            try:
                answer = int(input("You'r choice?: "))
            except Exception:
                logging.debug("Answer = %s" % answer)
                answer = -1
            len_columns = len(columns)
            logging.debug("Columns = %s" % columns)
            logging.debug("Len_columns = %s" % len_columns)
            logging.debug("Values_columns = %s" % values_columns)
            logging.debug("Answer = %s" % answer)
            if not answer:
                break
            if not (answer > len_columns) and answer > 0:
                if not columns[answer - 1] in values_columns:
                    print(values_columns.append(columns[answer - 1]), " was append")
            if answer > len_columns and not answer > (len(values_columns) + len_columns):
                print(values_columns.pop(answer - (1 + len_columns)), " was deleted")
            os.system('cls||clear')
        
        logging.debug("Values_columns = %s" % values_columns)
        if not values_columns:
            return
        values = []
        for val in values_columns:
            values.append(str(input("Please, endter " + str(val) + ": ")))
        try:
            excute_str = str("INSERT INTO " + table + " (" + ", ".join(values_columns) + ") " +
                        "VALUES ('" + "', '".join(values) + "')")
            logging.debug("Excute_str = %s" % excute_str)
            cur.execute(excute_str)
            conn.commit()
            print("Records inserted successfully")
            view(table)
        except (Exception, Error) as error:
            print("Error when working with PostgreSQL ", error)
            conn.rollback()
            
    #------Function add_product---------                
    
    #------Function update_product--------- 
    def update(table, req_id):
        '''
        Function for updating rows in a table. 
        Accepts the table and the id to change.
        '''
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + table)
        rows = cur.fetchall()
        logging.debug("Req_id = %s" % req_id)
        logging.debug("Table = %s" % table)
        cur.execute("SELECT column_name FROM information_schema.columns WHERE information_schema.columns.table_name='" + table + "';")
        columns = []
        for col in cur.fetchall():
            col = str(col)
            columns.append(col.replace('(', '').replace(')', '').replace(',', '').replace('\'', ''))
        logging.debug("Columns = %s" % columns)
        values_columns = []
        while True:
            input_num = 1
            print("Enter the number to add the item to the table " + table + ": ")
            for col in columns:
                print(input_num, ") ", col)
                input_num += 1
            print("\nOr enter the number to exclude from the append: ")
            for val in values_columns:
                print(input_num, ") ", val)
                input_num += 1
            print("\n0) Enter zero to exit\n")
            try:
                answer = int(input("You'r choice?: "))
            except Exception:
                logging.debug("Answer = %s" % answer)
                answer = -1
            len_columns = len(columns)
            logging.debug("Columns = %s" % columns)
            logging.debug("Len_columns = %s" % len_columns)
            logging.debug("Values_columns = %s" % values_columns)
            logging.debug("Answer = %s" % answer)
            if not answer:
                break
            if not (answer > len_columns) and answer > 0:
                if not columns[answer - 1] in values_columns:
                    print(values_columns.append(columns[answer - 1]), " was append")
            if answer > len_columns and not answer > (len(values_columns) + len_columns):
                print(values_columns.pop(answer - (1 + len_columns)), " was deleted")
            os.system('cls||clear')
        
        logging.debug("Values_columns = %s" % values_columns)
        if not values_columns:
            return
        values = []
        for val in values_columns:
            values.append(val + " = '" + str(input("Please, endter " + str(val) + ": ")) + "'")
        try:
            excute_str = str("UPDATE " + table +
                        " SET " + ", ".join(values) +
                        " WHERE id = " + str(req_id))
            logging.debug("Excute_str = %s" % excute_str)
            cur.execute(excute_str)
            conn.commit()
            print("Records inserted successfully")
            view(table)
        except (Exception, Error) as error:
            print("Error when working with PostgreSQL ", error)
            conn.rollback()
    #------Function update_product--------- 
    
    #------Function delete_product--------- 
    def delete_product(req_id):
        cur = conn.cursor()
        excute_str = str("DELETE FROM products WHERE id=" + req_id)
        cur.execute(excute_str)
        conn.commit()
    #------Function delete_product--------- 
    
    answer = print_menu()
    
    if answer == 1:
        os.system('cls||clear')
        print("View all")
        table = choose_table()
        if not table:
            print("Empty input")
        else:
            print("View all " + table)
            view(table)
    elif answer == 2:
        os.system('cls||clear')
        print("Add new product")
        table = choose_table()
        if not table:
            print("Empty input")
        else:
            add(table)
    elif answer == 3:
        print("Update product")
        table = choose_table()

        if not table:
            print("Empty input")
        else:
            view(table)
            try:
                answer = int(input("You'r choice?(id): "))
            except Exception:
                logging.debug("Answer = %s" % answer)
                print("Invalid value")
                continue
            os.system('cls||clear')
            update(table, answer)
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
        print("Invalid input. Please repeat again")
    os.system('pause')
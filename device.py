import mysql.connector
import argparse
import datetime
import random
from tabulate import tabulate
import time

SEND_INTERVAL = 5

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="cs198eth2",
    database="cs198trad"
)

mycursor = mydb.cursor()

# field_names = [i[0] for i in mycursor.description]
# field_names = mycursor.column_names
field_names = ["deviceID","timestamp","longitude (x)", "latitude (y)"]

def get_random_float():
    start = random.randint(1,100)
    end = random.randint(1,100)

    if start == end:
        end += 1
    elif start > end:
        start,end = end,start

    return random.uniform(start,end)

def insert_random_data(table,deviceID):
    x = get_random_float()
    y = get_random_float()
    time = datetime.datetime.now()
    str_time = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = f"INSERT INTO {table} (deviceID, timestamp, longitude, latitude) VALUES (%s, %s, %s, %s)"
    val = (deviceID,time,x,y)
    mycursor.execute(sql,val)
    mydb.commit()
    table = [field_names,list(val)]
    print(tabulate(table))
    print(mycursor.rowcount,"record inserted")

def read_latest(table):
    sql = '''SELECT * FROM gpsdata
    ORDER BY timestamp DESC LIMIT 1;'''
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result == None:
        print("You do not have any data yet!")
    else:
        print("latest GPS data:")
        table = [field_names,[result[0].strftime('%Y-%m-%d %H:%M:%S'),result[1],result[2]]]
        print(tabulate(table))

def read_all(table):
    sql = '''SELECT * FROM gpsdata
    ORDER BY timestamp DESC;'''
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(f"all GPS data:")
    table = [field_names]
    for x in result:
        table.append([x[0],x[1].strftime('%Y-%m-%d %H:%M:%S'),x[2],x[3]])
    print(tabulate(table))

def continous_send(table,deviceID):
    while True:
        insert_random_data(table,deviceID)
        time.sleep(SEND_INTERVAL)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', metavar='choice', type=str, required=True)
    parser.add_argument('-t', metavar='table', type=str, required=True)
    parser.add_argument('-d',metavar='deviceID',type=int,required=True)
    args = parser.parse_args()
    choice = args.c.lower()
    table = args.t
    deviceID = args.d
    if choice == "send" or choice == "1" or choice == "s":
        continous_send(table,deviceID)
    elif choice == "read_latest" or choice == "2" or choice == "l":
        read_latest(table)
    elif choice == "read_all" or choice == "3" or choice == "a":
        read_all(table)
    else:
        print(f"Incorrect arguments!")

if __name__ == '__main__':
    main()

import mysql.connector
import datetime
import random

mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    password="cs198eth2",
    database="cs198trad"
)

mycursor = mydb.cursor()

def get_random_float():
    start = random.randint(1,100)
    end = random.randint(1,100)

    if start == end:
        end += 1
    elif start > end:
        start,end = end,start

    return random.uniform(start,end)

def insert_random_data(table):
    x = get_random_float()
    y = get_random_float()
    time = datetime.datetime.now()
    str_time = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = f"INSERT INTO {table} (longitude, latitude, timestamp) VALUES (%s, %s, %s)"
    val = (x,y,time)
    mycursor.execute(sql,val)
    mydb.commit()

    # for args in ("longitude","latitude","datetime"), (x,y,str_time):
    #     print('{0:<9} {1:>8} {2:>8}'.format(*args))
    print("longitude\tlatitude\tdatetime")
    print(f'{x}\t{y}\t{str_time}')
    print("new record inserted")

def read_latest(table):
    sql = '''SELECT * FROM gpsdata
    ORDER BY timestamp DESC LIMIT 1;'''
    mycursor.execute(sql)
    result = mycursor.fetchone()
    print("latest GPS data:")
    print(f"{result[0]}\t{result[1]}\t{result[2].strftime('%Y-%m-%d %H:%M:%S')}")

insert_random_data("gpsdata")
read_latest("gpsdata")
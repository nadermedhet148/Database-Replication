import mysql.connector
import concurrent.futures
import threading
import random

connections = [
        mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin1234",
        port=6603,
        database="con3"
    ),
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin1234",
            port=6603,
            database="con4"
        ),
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin1234",
            port=6603,
            database="con2"
        ),
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin1234",
            port=6603,
            database="con1"
        ),
    
]

class PostDb:
    def __init__(self):
        pass

    def insertPost(self,name):
        selectedConnectionIndex = random.randrange(0,len(connections))
        connection = connections[selectedConnectionIndex]
        mycursor = connection.cursor()

        sql = "INSERT INTO post (name) VALUES (%s)"
        val = (name, )
        mycursor.execute(sql, val)

        connection.commit()
        print(mycursor._insert_id , " - record inserted with name : " , name)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for index in range(len(connections)):
                if(index != selectedConnectionIndex):
                    futures.append(executor.submit(self.__insertPostToReplica, id = mycursor._insert_id,  name=name,connection=connections[index]))


    def readPost(self,name):
        selectedConnectionIndex = random.randrange(0,len(connections))
        connection = connections[selectedConnectionIndex]

        mycursor = connection.cursor()

        sql = "Select * from post where name = %s"
        val = (name,)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)

# we send the id with the replice to avoid requests latency to override the id 
    def __insertPostToReplica(self,name,id,connection) :
        mycursor = connection.cursor()

        sql = "INSERT INTO post (id,name) VALUES (%s,%s)"
        val = (id,name, )
        mycursor.execute(sql, val)

        connection.commit()
        print(mycursor._insert_id , " - record inserted with name : " , name)



postDb = PostDb()

postDb.insertPost('name')
postDb.readPost('name')

postDb.insertPost('name2')
postDb.readPost('name2')

postDb.insertPost('name3')
postDb.readPost('name3')


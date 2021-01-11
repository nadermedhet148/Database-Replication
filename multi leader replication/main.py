import mysql.connector
import concurrent.futures
import threading
import random

dataCenters = [
    {
    "connection": mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin1234",
        port=6603,
        database="con2"
    ),
    "replications": [
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin1234",
            port=6603,
            database="con1"
        )
    ]
    },
     {
    "connection": mysql.connector.connect(
        host="localhost",
        user="root",
        password="Admin1234",
        port=6603,
        database="con3"
    ),
    "replications": [
        mysql.connector.connect(
            host="localhost",
            user="root",
            password="Admin1234",
            port=6603,
            database="con4"
        ),
    ]
}
]



class PostDb:
    def __init__(self):
        pass

    def insertPost(self, name):
        selectedDataCenterIndex = random.randrange(0,len(dataCenters))
        dataCenter = dataCenters[selectedDataCenterIndex]
        mycursor = dataCenter.get('connection').cursor()

        sql = "INSERT INTO post (name) VALUES (%s)"
        val = (name, )
        mycursor.execute(sql, val)

        dataCenter.get('connection').commit()

        print(mycursor._insert_id, " - record inserted with name : ", name , ' to master node')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for connection in dataCenter.get('replications'):
                futures.append(executor.submit(self.__insertPostToReplica,
                                               id=mycursor._insert_id,  name=name, connection=connection))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for dataCenterIndex in range(len(dataCenters)):
                if(dataCenterIndex != selectedDataCenterIndex):
                    futures.append(executor.submit(self.__insertPostToDataCenter,
                                                id=mycursor._insert_id,  name=name, dataCenter=dataCenters[dataCenterIndex]))

    def readPost(self, name):
        dataCenter = random.choice(dataCenters);
        mycursor = dataCenter.get('connection').cursor()

        sql = "Select * from post where name = %s"
        val = (name,)
        mycursor.execute(sql, val)

        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)

# we send the id with the replice to avoid requests latency to override the id
    def __insertPostToReplica(self, name, id, connection):
        mycursor = connection.cursor()

        sql = "INSERT INTO post (id,name) VALUES (%s,%s)"
        val = (id, name, )
        mycursor.execute(sql, val)

        connection.commit()
        print(mycursor._insert_id, " - record inserted with name : ", name , ' to replica node')

# we send the id with the replice to avoid requests latency to override the id
    def __insertPostToDataCenter(self, name, id, dataCenter):
        mycursor = dataCenter.get('connection').cursor()

        sql = "INSERT INTO post (id,name) VALUES (%s,%s)"
        val = (id,name, )
        mycursor.execute(sql, val)

        dataCenter.get('connection').commit()
        print(mycursor._insert_id, " - record inserted with name : ", name, ' to master node')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for connection in dataCenter.get('replications'):
                futures.append(executor.submit(self.__insertPostToReplica,
                                               id=mycursor._insert_id,  name=name, connection=connection))


postDb = PostDb()

postDb.insertPost('name')
# postDb.readPost('name')

# postDb.insertPost('name2')
# postDb.readPost('name2')

# postDb.insertPost('name3')
# postDb.readPost('name3')

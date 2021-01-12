# Database Replication :
__________________________

## Master slave replication :
____________________________________
Master-slave replication enables data from one database server (the master) to be replicated to one or more other database servers (the slaves). The master logs the updates, which then ripple through to the slaves. The slave outputs a message stating that it has received the update successfully, thus allowing the sending of subsequent updates. Master-slave replication can be either synchronous or asynchronous. The difference is simply the timing of propagation of changes. If the changes are made to the master and slave at the same time, it is synchronous. If changes are queued up and written later, it is asynchronous.
![MasterSlaveReplication](docs/dbreplication173.png)

## Multi leader replication :
____________________________________
We know in Leader follower model, client can able to write only by leader this if leader is down for any reason, you can't write to database.
To overcome this issue multi leader model was created which allows clients to send write requests to multiple leaders and is also called as multi leader replication. In this model, leaders will be simultaneously acts as a follower to other leaders

![MultiLeaderReplication](docs/1578341501794.png)

## Leader less replication (Dynamo-style) :
________________________________

Some data storage systems take a different approach, abandoning the concept of a leader and allowing any replica to directly accept writes from clients. Amazon used this leaderless architecture for its in-house Dynamo system. That’s why leaderless replication is often called Dynamo-style.
In some leaderless implementations:
---------------
the client directly sends its writes to several replicas,
while in others, a coordinator node  sends the writes to the replicas on behalf of the clients. Unlike a leader-based replication, the coordinator does not enforce a particular ordering of writes. And this difference in design has profound consequences for the way the leaderless architecture is used.

![MultiLeaderReplication](docs/image-2.png)

# Databus
This project is an asynchronous data integration platform. It can pull, queue, process and push data within the defined rules. It is very flexible - you can write your own factory or concrete classes easily.

![Databus Queue](screenshot.png?raw=true "Databus")

## Clients

It is currently used by [Eczacibasi Tuketim](https://www.eczacibasituketim.com) to accept various B2B documents over E-Mail and transfer them to SAP.

## Installation

First, install Vibhaga.

```
pip install git+http://github.com/keremkoseoglu/vibhaga.git
```

Then, install Databus.

```
pip install git+http://github.com/keremkoseoglu/databus.git
```

## Running databus
Running a databus instance is really easy! 

```
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
PrimalDispatcherFactory().create_dispatcher().start()
```

This will start Databus with the default configuration, which uses json_db. Visit http://127.0.0.1:5000 to see what it's been doing.

The default demo account is demo:demo. The default admin account is root:root. On a live system, you are advised to change this in your database.

To start Databus with a custom configuration, you can provide a dispatcher ticket. Here is an example.

```
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.dispatcher.abstract_dispatcher import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory

sql_args = {
    SqlDatabaseArguments.KEY_DATABASE: "Master",
    SqlDatabaseArguments.KEY_PASSWORD: "reallyStrongPwd123",
    SqlDatabaseArguments.KEY_SCHEMA: "databus",
    SqlDatabaseArguments.KEY_SERVER: "127.0.0.1,1433",
    SqlDatabaseArguments.KEY_USERNAME: "SA"
}

ticket = DispatcherTicket(
    p_database_module="databus.database.sql_db.sql_database",
    p_database_arguments=sql_args
)

PrimalDispatcherFactory().create_dispatcher(p_ticket=ticket).start()
```

Inspect from databus.dispatcher.abstract_dispatcher for more startup options.

## Components

### Database
Databus needs a database to store client and queue data. Out of the box, it supports:
- json_db: A custom written engine which stores the data on the disk as JSON files.
- sql_db: An engine to store data on a Microsoft SQL Server instance

You can implement your own database engine too. All you need to do is to derive a new class from databus.database.abstract_database. Remember passing your own module name to the dispatcher as seen above.

Databus has the ability to export data. Check the export menu on the Web interface.

### Client
Defines a client company using Databus. Each client can has its own reader / processor / pusher classes. A singular Databus instance can support multiple clients. 

To add a new client (called abc);
- json_db:
  - Create the folder /data/clients/abc
  - Create the subfolders and config file just like you see in /data/json_db/clients_demo
- sql_db:
  - Fill the SQL Server tables just like the 'demo' client

If a client doesn't have any users defined, this means that the authentication is not active. The web interface will allow any login for that client.

### Dispatcher
This is the main engine of Databus. When you start up the dispatcher, the program is running. It is responsible of scheduling & invoking drivers.

### Passenger
Passenger defines a data type to travel between systems. If you are pulling E-Mails and forwarding them to your target system, E-Mail is your passenger.

To implement a new passenger;
- Create a new class derived from databus.passenger.abstract_passenger
- Ensure that your .py file has only one class (which is the passenger)
- Ensure calling super().__init__()
- You may need to implement corresponding puller / processor / pusher classes as well
- Add the puller class to your client configuration
   - json_db: /data/json_db/clients/(client name)/config.json
   - sql_db: databus.passenger

## Puller
Puller classes are defined to fetch passengers from source systems. For each source system, you may implement your own puller class. Databus has a built-in abstract Exchange puller; which you can implement for your own purposes. 

To implement a new puller;
- Ensure that the corresponding passenger class exists. If not, create your passenger class first.
- Derive a new class from databus.puller.abstract_puller
- Ensure that your .py file has only one class (which is the puller)
- Ensure calling super().__init__()
- Add the puller class to your client configuration. 
   - json_db: /data/json_db/clients/(client name)/config.json
   - sql_db: databus.puller

### Queue
Just what it says. When you pull a new passenger, it is stored in the queue until it is succesfully pushed to the target system. Even after a succesful push, the passenger lingers in the queue for a while. You can determine the wait time per client. 

### Processor
A processor can do anything you want to do between a pull and push operation. Filtering data is a typical processor operation.

To implement a new processor;
- Ensure that the corresponding passenger & puller classes exist. If not, create them first.
- Derive a new class from databus.processor.abstract_processor
- Ensure that your .py file has only one class (which is the processor)
- Ensure calling super().__init__()
- Add the processor class to your client configuration. 
   - json_db: /data/json_db/clients/(client name)/config.json
   - sql_db: databus.processor

### Pusher 
Pusher classes are defined to send passengers to target systems. For each source system, you may implement your own pusher class. 

To implement a new pusher;
- Ensure that the corresponding passenger & puller classes exist. If not, create them first.
- Derive a new class from databus.pusher.abstract_pusher
- Ensure that your .py file has only one class (which is the pusher)
- Ensure calling super().__init__()
- Add the pusher class to your client configuration. 
   - json_db: /data/json_db/clients/(client name)/config.json
   - sql_db: databus.processor

### Web
Databus has a built-in Flask website, which shows log and queue data. Whenever the dispatcher is started, the web server is activated too. 

### Report
This package includes some useful classes for cases where you want to build your own reporting logic.

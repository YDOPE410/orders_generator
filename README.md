# orders_generator

## The program that generate history of orders
* Generate orders histories;
* Publish records to RabbitMQ;
* Records consuming from RabbitMQ queues;
* Insert records into database.

Order structure
--
Order:
```
    id - unique id of order
    direction - order direction(only buy or sale)
    cur_pair - name of currency pair
    status - status of order
    date - timestamp of status changing in milliseconds
    init_px - initial currency pair value
    init_volume - initial volume
    fill_px - filled currency pair value
    init_volume - filled volume
    description - order description
    tag - order tags
```
All orders records divided distributed between 3 zones:
* Red: Order started in previous periods of trading and finish in current period;
* Green: Order start and finish in same period;
* Blue: Order start in current period and finish in next periods.

Trading execute on period Friday-Tuesday except weekends.
# Getting started:

```bash
$ git clone https://github.com/YDOPE410/orders_generator.git
```
## Requirements

### Python
If it not exists install it. Download it from official site: https://www.python.org/
Or update it if yours python version less than 3.7. 

### Install additional modules
Application use some modules to work with RabbitMQ and MySQL. Use this command to install it.
```bash
$ pip install -r requirements.txt 
```

### RabbitMq
The program uses a message broker RabbitMQ.
Generated records are sent to broker queues.
If it not exists install it. Download it from official site: https://www.rabbitmq.com/download.html

### MySql
The program uses MySQL database management system. 
The generated data is read from the message broker queues and stored in MySQL.
If it not exists install it. Download it from official site: https://www.mysql.com/downloads/.

### Create database and tables
Use the SQL query from "create_database.sql" in your database client.

### Modify the configuration file (if necessary)
Change data in "config_default.json". You should to change "COUNT_ORDERS", "RED_ZONE", "GREEN_ZONE", "BLUE_ZONE", "BATCH", "MYSQL"."USER", "MYSQL"."PASSWORD", "RABBITMQ"."USER", "RABBITMQ"."PASSWORD".

### Running
To run the application use the command:
```bash
python3.7 launcher.py
```

#Docker start
## Requirements
### Docker
* Docker
* Docker Compose
Download it from official site: https://docs.docker.com/install/

## Running
Run MySQL and RabbitMQ services
```bash
$ docker-compose up
```
Build docker image
```bash
$ docker image --tag=orders_generator .
```
Run docker container
```bash
$ docker run --network=orders_generator_default orders_generator
```
##After finish application
Stop container and delete services created by docker-compose up
```bash
$ docker-compose down
```
Delete image if you want free up memory
```bash
$ docker image rm --force orders_generator
```
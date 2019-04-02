# orders_generator
Generator of orders history

Overview
--
Order:
    id - id of order
    direction - order direction
    cur_pair - name of currency pair
    init_px - initial currency pair value
    init_volume - initial volume
    fill_px - filled currency pair value
    init_volume - filled volume
    status - status of order
    date - time of status changing in milliseconds
    tag - order tags
    desription - order descriptionn

All orders records divided distributed between 3 zones:
* Red: Order started in previous periods of trading and finish in current period
* Green: Order start and finish in same period 
* Blue: Order start in current period and finish in next periods

Trading execute on period Friday-Tuesday except weekends




Install:

bash
$ git clone https://github.com/YDOPE410/orders_generator.git

Chech if python exists:
bash
$ python --version
If it not exists install it. Download it from official site: https://www.python.org/
Or update it if yours python version less than 3.7. 



Install additional modules
bash
$ pip install -r path_to/requirements.txt 

---
#Usage

Configurate generation settings before executing
:

Required settings:


// Change to your configurations

{
  "COUNT_ORDERS": 2000,
  "RED_ZONE": 0.15,
  "GREEN_ZONE": 0.6,
  "BLUE_ZONE": 0.25,
  "BATCH": 100,
  "MYSQL": {
    "DATABASE": "db_simcord_orders_history",
    "HOST": "localhost",
    "PORT": 3306,
    "PASSWORD": "",
    "USER": "hoffman"
  },
  "RABBITMQ": {
            "HOST": "localhost",
            "PORT": 5672,
            "VIRTUAL_HOST": "/",
            "PASSWORD": "",
            "USER": "hoffman",
            "EXCHANGE": "orders_by_statuses",
            "ROUTING_KEY": "topic"
        }),
  "LOG_TXT_FILE_PATH": "../logs/current_date.log",
  "LOG_LVL": 1
}


If you want you can change other parameters in your config.json file

## Starting history generation

$ python launcher.py


Result file content:
bash
(48331124, 'GBP/AUD', 'sale', 'new', '1550565487835', 1.8199, 0.0, 969, 0, 'License_change', 'pace')

(48331124, 'GBP/AUD', 'sale', 'to_provide', '1550565490742', 1.8199, 0.0, 969, 0, 'License_change', 'pace')

(48331124, 'GBP/AUD', 'sale', 'reject', '1550565493649', 1.8199, 0.0, 969, 0, 'License_change', 'pace')

(11668019, 'EUR/CAD', 'sale', 'new', '1550417433289', 1.5, 0.0, 589, 0, 'Technology_presentation', 'reset')

(11668019, 'EUR/CAD', 'sale', 'to_provide', '1550417435053', 1.5, 0.0, 589, 0, 'Technology_presentation', 'reset')

(11668019, 'EUR/CAD', 'sale', 'fill', '1550417436817', 1.5, 1.485, 589, 589, 'Technology_presentation', 'reset')

(34064294, 'GBP/AUD', 'sale', 'new', '1550573507947', 1.8199, 0.0, 990, 0, 'License_change', 'pace')

(34064294, 'GBP/AUD', 'sale', 'to_provide', '1550573510916', 1.8199, 0.0, 990, 0, 'License_change', 'pace')

(34064294, 'GBP/AUD', 'sale', 'reject', '1550573513885', 1.8199, 0.0, 990, 0, 'License_change', 'pace')

(9626267, 'AUD/USD', 'buy', 'new', '1550245820949', 0.7066, 0.0, 147, 0, 'new_accountant', 'short')

(9626267, 'AUD/USD', 'buy', 'to_provide', '1550245821389', 0.7066, 0.0, 147, 0, 'new_accountant', 'short')

(9626267, 'AUD/USD', 'buy', 'partial_fill', '1550245821829', 0.7066, 0.7277980000000001, 147, 144.06, 'new_accountant', 'short')

(991994, 'GBP/AUD', 'sale', 'new', '1550577558333', 1.8199, 0.0, 1000, 0, 'License_change', 'pace')

(991994, 'GBP/AUD', 'sale', 'to_provide', '1550577561333', 1.8199, 0.0, 1000, 0, 'License_change', 'pace')

(991994, 'GBP/AUD', 'sale', 'reject', '1550577564333', 1.8199, 0.0, 1000, 0, 'License_change', 'pace')

(8153135, 'GBP/AUD', 'sale', 'new', '1550576265927', 1.8199, 0.0, 997, 0, 'License_change', 'pace')

(8153135, 'GBP/AUD', 'sale', 'to_provide', '1550576268917', 1.8199, 0.0, 997, 0, 'License_change', 'pace')

(8153135, 'GBP/AUD', 'sale', 'reject', '1550576271907', 1.8199, 0.0, 997, 0, 'License_change', 'pace')

(25236710, 'GBP/CHF', 'sale', 'new', '1550494301478', 1.2914, 0.0, 786, 0, 'Director_change', 'hold')

(25236710, 'GBP/CHF', 'sale', 'to_provide', '1550494303836', 1.2914, 0.0, 786, 0, 'Director_change', 'hold')

(25236710, 'GBP/CHF', 'sale', 'reject', '1550494306194', 1.2914, 0.0, 786, 0, 'Director_change', 'hold')

(16822679, 'GBP/USD', 'buy', 'new', '1550234854905', 1.2858, 0.0, 119, 0, 'new_accountant', 'short')

(16822679, 'GBP/USD', 'buy', 'to_provide', '1550234855260', 1.2858, 0.0, 119, 0, 'new_accountant', 'short')

(16822679, 'GBP/USD', 'buy', 'partial_fill', '1550234855615', 1.2858, 1.35009, 119, 116.62, 'new_accountant', 'short')


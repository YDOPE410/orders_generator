CREATE DATABASE IF NOT EXISTS db_simcord_orders_history;

USE db_simcord_orders_history;

DROP TABLE IF EXISTS history;

CREATE TABLE history (
  id int NOT NULL AUTO_INCREMENT,
  order_id bigint NOT NULL,
  cur_pair varchar(255) NOT NULL,
  direction varchar(255) NOT NULL,
  status varchar(255) NOT NULL,
  date bigint NOT NULL,
  init_px double NOT NULL,
  fill_px int NOT NULL,
  init_vol float NOT NULL,
  fill_vol int NOT NULL,
  description varchar(255) NOT NULL,
  tag varchar(255) NOT NULL,
  PRIMARY KEY (id)
);
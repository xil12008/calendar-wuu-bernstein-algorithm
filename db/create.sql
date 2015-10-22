CREATE DATABASE ds;
USE ds;
CREATE TABLE logs(
	id INT NOT NULL AUTO_INCREMENT,
	node INT NOT NULL,
	time_stamp INT NOT NULL,
	log VARCHAR(255) NOT NULL,
	PRIMARY KEY ( id ));
CREATE TABLE appointments(
	id INT NOT NULL AUTO_INCREMENT,
	app_name VARCHAR(255) NOT NULL UNIQUE,
	day INT NOT NULL,
	start_time INT NOT NULL,
	end_time INT NOT NUll,
	participants VARCHAR(255) NOT NULL,
	PRIMARY KEY ( id ));
CREATE TABLE time(
	id INT NOT NULL AUTO_INCREMENT,
	node_id INT NOT NULL UNIQUE,
	node0 INT NOT NULL,
	node1 INT NOT NULL,
	node2 INT NOT NULL,
	node3 INT NOT NULL,
	PRIMARY KEY ( id ));

INSERT INTO time (node_id, node0, node1, node2, node3) VALUES (0,0,0,0,0);
INSERT INTO time (node_id, node0, node1, node2, node3) VALUES (1,0,0,0,0);
INSERT INTO time (node_id, node0, node1, node2, node3) VALUES (2,0,0,0,0);
INSERT INTO time (node_id, node0, node1, node2, node3) VALUES (3,0,0,0,0);

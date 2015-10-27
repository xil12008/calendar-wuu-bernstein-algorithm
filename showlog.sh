#!/bin/bash

mysql -u root -e 'select * from logs;' ds 
mysql -u root -e 'select * from appointments;' ds 
mysql -u root -e 'select * from time;' ds 

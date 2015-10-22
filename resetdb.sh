#!/bin/bash

mysql -u root < db/drop.sql
mysql -u root < db/create.sql

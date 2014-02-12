#!/bin/sh
db="mysql"
host="localhost"
user="querymgr"
pwd=''
pmt='--prompt=\R:\m:\s-\U-\d-MySQL>'
charset='--default-character-set=utf8'
mysql -h$host -u$user -p$pwd $db $pmt $charset


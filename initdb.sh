#!/bin/sh

exec psql -h localhost -p 5432 -U postgres -s stock_mon -f init_db.sql

# Setting up Postgres

### A couple key concepts you need to understand first:
 - There are unix/linux users.  When you ssh or open a terminal you typically see your username and host (eg `aelmore@addison`)
 - When you install postgres on ubuntu, it creates a postgres linux user  that you become (su postgres) and then connect to postgresql by just typing `psql`.
 This user is effectively the superuser of your new postgresql server
 - You will be creating a user inside of postgres and modifying a configurtion in postgresql to allow this new user to connect to postgresql
 - You need to restart or reload postgres to pick up changes you make to configuration files.
 - You will need to edit configuration files either as the *linux* user postgres or do as sudo.  This might be using nano, vi, or sudo gedit (if you have a gui)
 - In a prior homework you installed a postgresql client called `psql`. This application allows you to connect to postgresql to issue commands and sql.
 Installing a postresql server will set this up by default.
 - Some of the instructions require you to be in psql, some of them will require you to be in the command line.
 - note that psql needs a ; at the end of most statements
 
 
I would suggest making sure the following things work (in order) to make sure your postgres is set up. The examples are not tested for correctness!

### Create a database and user
 - Install postgresql-server 9.5+ (it is available on Ubuntu 16.04),your version maybe higher, but we will document as 9.5. **Change accordingly.**
 - Also for these instructions we will be using testdb as the database name and cappuser as the username. You can use whatever you want.
 - ```sudo su postgres``` (now you are logged in as the postgres user)
 - run: ```$ psql``` as the postgres user
 - create a test database (```create database testdb;```)
 - connect to the test database: ```\c testdb```
 - create a test table: ```create table test (id int);```
 - insert one row: ```insert into test values(1);```
 - run a query: ```select * from test;```
 - exit psql ```\q```
 - in linux, change the configuration files (at /etc/postgresql/9.5/main/ )
   - postgresql.conf (chage the line replace localhost with *): `listen_addresses = '127.0.0.1'`  # what IP address(es) to listen on; (**only need if you want to connect from other addresses than locally**)
   - pg_hba.conf to allow a user to connect with a password:
 - You must add these lines at the end of pg_hba.conf (note the database name and database user):
   ```
   host    testdb     cappuser        127.0.0.1/32            md5
   local    testdb     cappuser                    md5
   ```
   
 - note that you can use all for database name
 - The above configuration is saying allow user cappuser to connect to database testdb from IP address 127.0.0.1 only. You could change the host to be 0.0.0.0/32 to allow cappuser to connect to testdb from any host address
 - Exit from user postgres and go back to your main user (```exit```). verify with whoami
 - restart or reload your database to pick up the changes (from the main account, not the postgres one): ```sudo service postgresql restart```
 - get a user created with a password (this is a bit a of a pain look at something like http://www.cyberciti.biz/faq/howto-add-postgresql-user-account/ you need to add the user and give the user permissions to read and write from the database. giving the user superuser rights, might make it easier -- but be careful with this in general)
  - login as postgres: ```sudo su postgres```
  - run: ```psql``` (you should be logged in as postgres)
  - ```create user cappuser with encrypted password 'XXX';``` (with XXX as your password wrapped in single quotes)
  - ```alter user cappuser login;```
  - ```alter database testdb owner to cappuser;``` (if you already created this database)
  - ```GRANT ALL PRIVILEGES ON DATABASE testdb TO  cappuser;```
  - ```\c testdb``` (this says connect to databse testdb)
  - ```GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cappuser;```
  - ```GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cappuser;```
  - ```\q``` (leave psql)
  - ```psql -U cappuser -d testdb -W -h 127.0.0.1``` (enter your password)   (this verifies you can connect to postgresql using your newly created user).
  - ```select * from test;```
  - now you have verified you are able to login to postgresql as cappuser
 - test your user from psql not as the postgres user, (exit if you are currently postgres) ( psql -U [yourusername] -W -d testdb -h 127.0.0.1 ) the -U is the user name, -W says ask for my password, -d is here is the database name, -h is the host address
 - connect remotely via: psql -U [yourusername] -W  -h [the IP or address of your VM] -d testdb (if you are setting up remote connection, we are not right now)
 - write a dead simple python program that connects to your database via a hostname/IP and issues the same test query

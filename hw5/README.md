# HW 5

### Due 5/14/2017 11:59 pm CST

In this assignment you'll learn how to install and set up PostgeSQL 9.x on an ubuntu/debian server, configure access to a postgres database, and load and analyze lobbying data from the City of Chicago via a python interface/application to postgres. The data is randomized from the city of Chicago's lobbying dataset.

## Collaboration Policy

You can work with one other person on this assignment. However **both** partners are expected to understand all of the code and be able to run the code. We will sample students after the assignment to show us the running VM in their laptop. You should register as a team for this assignment on chisubmit.

## To run
 - `python driver.py`
 - See help on options to running the program `python driver.py --help`
 - Phases run in the program are (in order) load, ops, and analyze, you can skip phases for testing (see --help).  *Note that the ops phase (reading and inserting records) will be run with concurrent clients.*
 - Other parameters that might help with debugging: debug, limit_ops, and processes (set to 1)
 - Note if you want to add output in LobbyDBClient.py code please use logger.debug and set the debug parameter

## Requirements
 - Install Python 2.7
 - Install PostgreSQL 9.X and set up
 - Install python pandas
 - Install python hdrhistogram
 - Install python numpy
 - Install python to postgresql library (there are several option, psycopg2 is a popular choice)

## Tasks

### Step 0
 - Set up an Ubuntu VM or OS (16.04+ preferred). 10GB of storage needed
 - Install, configure, and verify postgres(psql) install. See [psql.md](psql.md)
 - Create the database using the prior instructions

### Step 1
 - Look at the function calls in LobbyDBClient and [dataset.md](dataset.md), design an E-R diagram to satisfy the data requirements primarily based on the LobbyDBClient (the full dataset has more than what we use).
 - **Add the ER diagram** as lobby-er.pdf or lobby-er.jpg
 - Create the physical schema with a set of DDL statements in a file called createDB1.sql (make sure this file is what you use
   to create your database) *do not optimize the schema at all outside of primary keys*
 - Place both files in **hwfiles directory**.

### Step 2
 - Implement the functions in LobbyDBClient.py
 - You can disable operations for testing load operations only by passing --skipops and --skipanalyze to the driver.py
 - Run the full database driver and save the output via python driver.py | tee hwfiles/out1.log
 - Use best practices for interacting with a database via python. (search online)

### Step 3
 - Optimize the database by adding indexes or other optimizations (don't worry about tuning dbms settings or isolation levels)
 - Create a new DDL file with the optimizations in hwfiles/createDB2.sql
 - Run the full database driver and save the output via python driver.py | tee hwfiles/out2.log

## Important Submission Note
You must make sure any added files (out1,out2, erds, etc are added and committed in git. Submissions without these files will be graded as if you did not do this step!)

### General tips
The functions are intentionally not well designed to map to an ideal ERD. You may need to tease out what functions are updating and inserting what entities...

You typically need to do the create database outside the ddl file.

You can (and should) run the ddl file against your db something like:

 `psql mydb [all your parameters to connect]< mydll.sql`

You should put ```drop table if exists [TABLENAME];``` statements in the start of your ddl file to clean up tables from an old setup (eg recreate a clean/fresh database ).

If you do not understand the following linux concepts you may want to read up on them or come to office hours:
 - linux users and permissions. running whoami to see who i am logged in as
 - ls, cd, mv, rm, -rf, mkdir,  cp
 - su   ( to switch users/ switch to root)
 - When do you need sudo and what sudo is
 - CTRL D and CTRL C to quit programs
 - How to write and quit in vi or vim (or install nano)
 - What an IP address and port are

Its generally a good idea to create a cursor for each query/function. They are relatively lightweight, while the connections are expensive and should be saved. See psycopg docs: http://initd.org/psycopg/docs/faq.html#best-practices

Close connections when you know you are done or if your program will crash/halt

When casting data types you should wrap them in a try, catch block. If a bad string is passed, your program would crash.

Multi-line SQL statements can be enclosed in """ """  (this is for long strings in Python)

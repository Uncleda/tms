# TMS(terminal management system)
====
A python web console to manage the VDI teminals, which currently support Linux based terminal.

### Dependencies
base on `python2.7.5`, `Django1.9`, `fabric1.0`, and `MySQL`

### Getting start
1. download the source code;
2. create database and modity the database configuration in setting file;
3. change the `env.user` and `env.password` in fabfile file;
4. create database tables:
    ```
    python manage.py makemigrations tmsApp
    python manage.py migrate tmsApp
    ```
4. create a super user:
    ```
    python manage.py createsuperuser
    ```
5. modify the shell scrip runserver based on your test environment and just run:
    ```
    ./runserver
    ```
   It would start the server like this:

   *January 06, 2016 - 06:44:22*
   *Django version 1.9, using settings 'tms.settings'*
   *Starting development server at http://IP:PORT/*
   *Quit the server with CONTROL-C.*

6. Copy the URL address http://IP:PORT/admin to your browser address.

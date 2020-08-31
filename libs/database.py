import psycopg2
import os
import logging

logging.basicConfig(filename='./logs/voice.log',level=logging.DEBUG)

def create_table_command():
    commands = (
        '''
        CREATE TABLE IF NOT EXISTS servers (
        id SERIAL PRIMARY KEY,
        name VARCHAR(55) NOT NULL,
        description text NOT NULL
        )''',
        '''
        CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        ip_address VARCHAR(55) NOT NULL,
        name VARCHAR(55) NOT NULL,
        description text NOT NULL
        )''',
        '''
        CREATE TABLE IF NOT EXISTS voices (
        id SERIAL PRIMARY KEY,
        uuid uuid NOT NULL,
        project_id integer REFERENCES projects (id),
        server_id integer REFERENCES servers (id),
        date VARCHAR(55) NOT NULL,
        time VARCHAR(55) NOT NULL,
        duration FLOAT NOT NULL,
        dbSet BOOLEAN NOT NULL,
        ckeckAO VARCHAR(5) NOT NULL,
        checkWord VARCHAR(5) NOT NULL,
        phone VARCHAR(55) NOT NULL
        )'''
    )
    return commands

def insertRecord():
    commands = '''
    INSERT INTO voices (uuid, date, time, duration, dbSet, ckeckAO, checkWord, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    return commands

def db_connect(data):
    try:
        commands = create_table_command()
        insertColumn = insertRecord()
        conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" %(os.getenv("DBNAME", ''), os.getenv("HOST", ''), os.getenv("DBUSER", ''), os.getenv("PASSWORD", '')))
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        for command in commands:
            cursor.execute(command)
        if(data):
            cursor.execute("INSERT INTO voices (uuid, date, time, duration, dbSet, ckeckAO, checkWord, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (data["uuid"], data["date"], data["time"], data["duration"], data["dbSet"], data["ckeckAO"], data["checkWord"], data["phone"]))
            print('Запись сохранена в базе')
        conn.commit() # <--- makes sure the change is shown in the database
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
       logging.error(error)
    finally: 
        if conn is not None: 
            conn.close() 
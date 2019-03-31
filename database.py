import sqlite3 # https://docs.python.org/2/library/sqlite3.html
import pathlib
import os

class Database:

    database_file_name = None

    def __init__(self, database_file_name=''):
        if not database_file_name:
            return
        
        self.database_file_name = database_file_name
        self.database_file_path = pathlib.Path(self.database_file_name)

    def run_sql_commands(self, commands=[]):
        for sql_command, *arg_tuple in commands:
            self.cursor.execute(sql_command, tuple(arg_tuple))
        return self.connection.commit()
    
    def run_sql_command_many_data(self, sql_command, data_list=[]):
        self.cursor.executemany(sql_command, data_list)
        return self.connection.commit()
    
    def down(self):
        self.connection.close()
    
    def exist(self):
        return self.database_file_path.exists()
    
    def delete(self):
        if self.exist():
            os.remove(self.database_file_path.absolute())
    
    def up(self):
        self.connection = sqlite3.connect(self.database_file_name)
        self.cursor = self.connection.cursor()

class DatabaseManager:

    db_name = 'my-database.sqlite'
    database_object = None

    def __init__(self, *args, **kwargs):
        self.db = Database(self.db_name)

        self.prepare_database_and_schema()
        
    def get_or_create(self, table_name, db_object):
        if self.db.connection and self.db.cursor:
            self.db.run_sql_commands([
                ('INSERT INTO {} ({}) VALUES ({});'.format(
                    table_name,
                    # insert question marks for field
                    ','.join(db_object.keys()),
                    # insert question marks for value
                    ','.join(['?'] * len(db_object)),
                ),) +
                # value tuples
                tuple(db_object.values())
            ])
            return
    
    def prepare_database_and_schema(self):
        # debug (if cache is enabled, delete this line)
        # self.db.delete()

        # create database
        self.db.up()

        # create schema for tables
        self.db.run_sql_commands([
            ('''CREATE TABLE States (
                id INTEGER PRIMARY KEY,
                Name TEXT
            );
            ''',),
        ])
        self.db.run_sql_commands([
            ('''CREATE TABLE Sites (
                id INTEGER PRIMARY KEY,
                Name TEXT,
                Type TEXT,
                Description TEXT,
                Location TEXT,
                
                StateID INTEGER,
                FOREIGN KEY (StateID) REFERENCES States(id)
            );
            ''',),
        ])
        self.db.run_sql_commands([
            ('''CREATE TABLE SitePages (
                id INTEGER PRIMARY KEY,
                Url TEXT,
                IsDone INTEGER
            );
            ''',),
        ])

        return self.db
    
    def wipe_database(self):
        self.db.delete()
        return
    
    def export_site_to_csv(self):
        # TODO
        return
    
    def is_page_complete(self, url):
        """
            check if the url is completed.
            will try to get that url from table `CompletedPage`.
            if it's there, it means the page is completed, and should return TRUE.
        """
        return False
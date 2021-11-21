import sqlite3
from sqlite3 import Error

import json

class FacultyDatabase:

    def __init__(self):
        pass


    def open_connection(self):
        """ create a database connection to a SQLite database """
        conn = json_data = None

        with open("../../../config/config.json", "r") as jsonfile:
            json_data = json.load(jsonfile)

        # print(json_data)

        db_file = json_data.get("db_filename", "")
        db_file = "../../../data/sqlite3/" + db_file

        # print("Database file: ", db_file)

        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

    def close_connection(self, conn):
        try:
            if conn:
                conn.close()
        except Error as e:
            print(e)


    def add_faculty_info(self, info):

        faculty_info_table = """ CREATE TABLE IF NOT EXISTS faculty_info (
                                                                            id integer PRIMARY KEY,
                                                                            name text NOT NULL,
                                                                            email text,
                                                                            phone text,
                                                                            university text NOT NULL,
                                                                            location text,
                                                                            expertise text NOT NULL,
                                                                            last_modified_date text
                                                                        );"""

        pass

    def add_faculty_biodata(self, biodate):
        pass

    def get_faculty_biodata(self):
        pass

    def get_faculty_info(self):
        pass




if __name__ == '__main__':
    faculty_db = FacultyDatabase()
    conn = faculty_db.open_connection()
    faculty_db.close_connection(conn)

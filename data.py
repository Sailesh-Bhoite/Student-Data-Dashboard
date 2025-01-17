"""
This module holds the functions which will interact with the database.
"""

import sqlite3
# Setting up the database connection.
conn = sqlite3.connect('students.db')

# Creating a cursor to execute queries.
c = conn.cursor()


def display_records():
    """ This function will return list of tuple of all the records present in the database """
    c.execute("SELECT * FROM Personal ORDER BY RollNo")
    all_records = c.fetchall()
    return all_records

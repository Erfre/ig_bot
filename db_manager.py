"""This class handles all the connections to the database."""
import random
import sqlite3
from sqlite3 import Error
from random import randint
from shutil import rmtree

class db_manager(object):
    """docstring for db_manager.

    This class handles all the connections to the database.
    """

    def __init__(self, dir_db):
        """Initilize.

        :param dir_db: directory for database
        """
        super(db_manager, self).__init__()
        self.dir_db = dir_db
        self.table = ""
        self.max_id = ""
        self.min_id = ""

    def create_connect(self):
        """Create db connection to sqlite database."""
        try:
            conn = sqlite3.connect(self.dir_db)
            return conn
        except Error as e:
            print(e)

        return None

    def delete_row(self, conn, row):
        """Deletes entry in database""" # Also have to delete image from computer
        id = row[0]
        path = row[1]
        c = conn.cursor()
        c.execute('DELETE FROM ' + self.table + ' WHERE id=:id', {"id": id})
        conn.commit()
        rmtree(path)

    def count_row(self,conn):
        self.max_id = self.get_max(conn)
        self.min_id = self.get_min(conn)
        return

    def get_max(self, conn):
        """Retrieves the max id in the table"""
        c = conn.cursor()
        c.execute('SELECT max(id) FROM ' + self.table)
        max = c.fetchone()[0]

        return max

    def get_min(self, conn):
        """Retrieves the min id in the table."""
        c = conn.cursor()
        c.execute('SELECT min(id) FROM ' + self.table)
        min = c.fetchone()[0]
        return min


    def get_random_row(self, conn, reviewed):
        """Returns a random row from table"""
        c = conn.cursor()

        while True: # this needs to be the min id
            id = randint(self.min_id, self.max_id)
            try:
                c.execute('SELECT * FROM ' + self.table + """ WHERE id=:rand
                  AND reviewed=:rv""", {"rand": id, "rv": reviewed})
                row = c.fetchone()
                if row is not None:
                    return row
                else:
                    continue
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print("Looks like this id doesn't exist")
                continue

    def get_random_id(self, conn):
        """Return a random id within the database limit.

        :param conn:
        """
        cur = conn.cursor()
        cur.execute('SELECT * FROM ' + self.table)
        tot_rows = cur.fetchall()
        return random.randrange(1, len(tot_rows))

    def close_connection(self, conn):
        """Closes the connection and saves the changes"""
        cursor = conn.cursor()
        cursor.commit()
        cursor.close()
        del cursor
        conn.close()
        return
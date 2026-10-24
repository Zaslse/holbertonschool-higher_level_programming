#!/usr/bin/python3
"""List states matching the user-supplied name using formatted SQL."""
import sys
import MySQLdb


if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost", port=3306,
                         user=sys.argv[1], passwd=sys.argv[2],
                         db=sys.argv[3], charset="utf8")
    cursor = db.cursor()
    query = "SELECT * FROM states WHERE name = '{}' ORDER BY id ASC".format(
        sys.argv[4])
    cursor.execute(query)
    for state in cursor.fetchall():
        print(state)
    cursor.close()
    db.close()

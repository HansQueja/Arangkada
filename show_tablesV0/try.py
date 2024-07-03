#trial file for querying
#when specifying attributes, dont use quotation marks


import sqlite3

conn = sqlite3.connect('transportV1.db')
conn.row_factory = sqlite3.Row #allows the db to be referenced by column names
c = conn.cursor()

query = input("Insert Query: ")
c.execute(query)
table = c.fetchall()

for row in table:
    print(dict(row))


conn.commit()

conn.close()
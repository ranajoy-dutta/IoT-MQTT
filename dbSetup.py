import sqlite3

try:
    conn = sqlite3.connect("mydb.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE dataTable ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, state TEXT(5), timestamp INTEGER)")

    conn.commit()
    cur.close()
    conn.close()
    print("Table Successfully Created!")
except Exception as e:
    print("An error occurred!\n",
          "Reason : ",e)

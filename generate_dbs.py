import sqlite3


def create_tax_database():
    connection = sqlite3.connect("taxrates.sqlite")
    crsr = connection.cursor()
    table = crsr.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='taxrates';"
    ).fetchall()
    if table != []:
        crsr.execute("DROP TABLE taxrates;")
    sql_command = """CREATE TABLE taxrates (
    ROWID PRIMARY KEY,
    state VARCHAR(2),
    county VARCHAR(20),
    taxrate FLOAT);"""

    crsr.execute(sql_command)
    connection.commit()

    states = ["NY", "WA"]
    counties = ["Monroe County", "King County"]
    taxrates = [0.0316, 0.0105]
    for i in range(2):
        rowid = states[i] + "-" + counties[i]
        print(rowid)
        crsr.execute(
            "INSERT INTO taxrates VALUES (?,?,?,?);",
            (rowid, states[i], counties[i], taxrates[i]),
        )
    connection.commit()
    connection.close()
    print("taxrate database created")


def create_retry_database():
    connection = sqlite3.connect("retry.sqlite")
    crsr = connection.cursor()
    table = crsr.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='retry';"
    ).fetchall()
    if table != []:
        crsr.execute("DROP TABLE retry;")
    sql_command = """CREATE TABLE retry (
    url PRIMARY KEY,
    failure_reason VARCHAR(20));"""
    crsr.execute(sql_command)
    connection.commit()
    connection.close()
    print("retry database created")

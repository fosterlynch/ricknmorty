import sqlite3
import logging


def create_tax_database():
    connection = sqlite3.connect("./databases/taxrates.sqlite")
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


def update_tax_database(state: str, county: str, taxrate: float):
    try:
        assert "County" in county
    except AssertionError as err:
        logging.error(err)
    rowid = state + "-" + county
    connection = sqlite3.connect("./databases/taxrates.sqlite")
    crsr = connection.cursor()
    crsr.execute(
        "INSERT INTO taxrates VALUES (?,?,?,?);",
        (rowid, state, county, taxrate),
    )


def create_retry_database():
    connection = sqlite3.connect("./databases/retry.sqlite")
    crsr = connection.cursor()
    table = crsr.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='retry';"
    ).fetchall()
    if table != []:
        crsr.execute("DROP TABLE retry;")
    sql_command = """CREATE TABLE retry (
    url VARCHAR(50) PRIMARY KEY,
    failure_reason VARCHAR(20));"""
    crsr.execute(sql_command)
    connection.commit()
    connection.close()
    print("retry database created")


update_tax_database("WA", "Spokane County", 0.012)

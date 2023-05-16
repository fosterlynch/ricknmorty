import sqlite3


class TaxRates:
    def __init__(self, county, state):
        self.county = county
        self.state = state
        self.taxrate = 0

        if self.county == "Monroe County" and self.state == "NY":
            self.taxrate = 0.0316
        if self.county == "King County" and self.state == "WA":
            self.taxrate = 0.0105


init = True

connection = sqlite3.connect("taxrates.sqlite")

if init:
    crsr = connection.cursor()
    crsr.execute("DROP TABLE taxrates;")
    sql_command = """CREATE TABLE taxrates (
    ROWID PRIMARY KEY,
    state VARCHAR(2),
    county VARCHAR(20),
    taxrate FLOAT);"""

    crsr.execute(sql_command)
    connection.commit()

# crsr = connection.cursor()

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

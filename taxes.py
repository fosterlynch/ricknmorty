import sqlite3
from api import RedFin
import logging


def find_tax_rate(connection, redfin: RedFin):
    """get country and state from redfin class, see if that entry exists in the database
    if it does, return the tax rate for downstream expenses estimation
    if not, figure that out later. # TODO

    Args:
        connection (_type_): sqlite connection to taxrate database
        Redfin (_type_): redfin class containing county and state information
    """
    crsr = connection.cursor()
    taxrate = crsr.execute(
        "SELECT taxrate FROM taxrates WHERE state=(?) AND county=(?)",
        (redfin.address[0], redfin.county),
    ).fetchall()
    if taxrate == []:
        logging.warning(
            "no tax information found, saving url for later retries in retry.sqlite"
        )
        save_url_for_retry(redfin)
    return taxrate


def save_url_for_retry(redfin):
    connection = sqlite3.connect("retry.sqlite")
    crsr = connection.cursor()
    crsr.execute(
        "INSERT INTO retry VALUES (?,?);", (redfin.url, "no_tax_rate")
    )
    connection.commit()
    connection.close()

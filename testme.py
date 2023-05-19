from realestate import House, Webvalues

from api import fetch_data_with_url
from api import RedFin
from taxes import find_tax_rate
import sqlite3
import json
import logging


with open("devurls.json", "r") as J:
    urls = json.load(J)
for url in urls:
    redfin_webdata = fetch_data_with_url(url)

    conn = sqlite3.connect("taxrates.sqlite")
    taxrate = find_tax_rate(conn, redfin_webdata)
    print(taxrate)
    # print(response.json())
    webvalues = Webvalues(  # why pass it into another dataclass?d
        list_price=redfin_webdata.price,
        property_type=redfin_webdata.property_type,
        investment_type="pure_investment",
        rentroll=[0],
        insurance=53,
        taxes=(redfin_webdata.price * 0.6 * taxrate)
        / 12,  # the .6 denotes assessed value
        hoa=0,
        interest_rate=0.07,
    )

    house = House(webvalues=webvalues)
    print("address", redfin_webdata.address)
    house.analyze()

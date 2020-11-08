"""Get information about ORP population total and 65+ from czso.cz."""

# Note: this file is not supposed to be run regularly (the data changes only once a year)

import csv
from lxml import html
import requests
import pandas as pd

# get list of ORPs
url = "http://apl.czso.cz/iSMS/cisexp.jsp?kodcis=65&typdat=0&cisvaz=80007_97&datpohl=08.11.2020&cisjaz=203&format=2&separator=%2C"
orps = pd.read_csv(url, encoding="cp1250")

# create list of ORPs and their population
with open("orp_population.csv", "w") as fout:
    header = ['code', 'name', 'population', 'population_65']
    dw = csv.DictWriter(fout, header)
    dw.writeheader()
    for row in orps.iterrows():
        code = row[1]['CHODNOTA']
        name = row[1]['TEXT']
        url = "https://vdb.czso.cz/vdbvo2/faces/cs/embeded.jsf?page=pozice-profilu&notSessConn=true&ewr=false&rn=N&rp=true&rz=true&rouska=false&u=__VUZEMI__65__" + str(code) + "&pvo=PU-DEM-OB1&z=T&f=TABULKA&clsp=31550&katalog=31550"
        r = requests.get(url)
        tree = html.fromstring(r.content)
        population = tree.xpath('//td/span/text()')[5].replace('\xa0', '')
        population_65 = tree.xpath('//td/span/text()')[39].replace('\xa0', '')
        item = {
            'code': code,
            'name': name,
            'population': population,
            'population_65': population_65
        }
        dw.writerow(item)
        # print('downloaded ' + str(code) + "/" + name)
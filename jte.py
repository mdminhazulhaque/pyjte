#!/usr/bin/env python3

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

"""
Copyright (c) 2018 Md. Minhazul Haque
This file is part of mdminhazulhaque/bd-mrp-api
(see https://github.com/mdminhazulhaque/banglalionwimaxapi).
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import tabulate

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def jte_info(billcode):
    session = requests.Session()
    response = session.get("https://www.jtexpress.my/track")
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find('input', {'name': '_token'}).get('value')
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'text/html,application/xhtml+xml,application/xml'
        }
    data = {
        '_token': token,
        'billcode': billcode
        }
    response = session.post('https://www.jtexpress.my/track', headers=headers, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    timeline = soup.find('div', {'class': 'timeline'})
    data = []
    for entry in timeline:
        try:
            date = entry.find("h3").text
            others = entry.find_all("p")
            time = others[0].text
            desc = others[1].text
            city = others[2].text.replace("City : ", "")
            state = others[3].text
            data.append([date, time, desc, city, state])
        except Exception as e:
            pass
    t_headers = "Date Time Description City State".split(" ")
    print(tabulate.tabulate(data, headers=t_headers))

if __name__ == "__main__":
    import sys
    billcode = sys.argv[1]
    jte_info(billcode)

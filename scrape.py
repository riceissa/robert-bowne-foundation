#!/usr/bin/env python3

import requests
import csv
from bs4 import BeautifulSoup
import re
import sys


def main():
    fieldnames = ["year", "main_heading", "italic_heading", "donee", "amount", "donee_url"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    url = "https://www.robertbownefoundation.org/grants.php"

    for year in range(2001, 2015):
        response = requests.post(url, data={"year": year})
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find_all("table")[1]
        main_heading = None
        italic_heading = None
        for row in table.find_all("tr"):
            if row.h1:
                main_heading = row.h1.text.strip()
                italic_heading = None
            elif row.h3:
                italic_heading = row.h3.text.strip()
            elif re.match("Total .*:$", row.find("td").text.strip()):
                # These are the rows that say e.g. "Total Direct Service: $95,000",
                # which are redundant since we already know the individual
                # grants. So skip them.
                pass
            elif not row.find("td").text.strip():
                # The table inserts these blank rows to create spacing, so ignore them
                pass
            else:
                donee, amount, donee_url = list(map(lambda x: x.text.strip(), row.find_all("td")))
                writer.writerow({
                    "year": year,
                    "main_heading": main_heading,
                    "italic_heading": italic_heading,
                    "donee": donee,
                    "amount": amount,
                    "donee_url": donee_url
                })


if __name__ == "__main__":
    main()

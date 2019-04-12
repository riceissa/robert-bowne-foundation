#!/usr/bin/env python3

import csv
import sys

def main():
    with open(sys.argv[1], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        print("""insert into donations (donor, donee, amount, donation_date, donation_date_precision, donation_date_basis, cause_area, url, notes) values""")
        first = True

        for row in reader:
            assert row["amount"].startswith("$")
            amount = float(row["amount"].replace("$", "").replace(",", ""))

            notes = row["main_heading"] + (" – " + row["italic_heading"] if row["italic_heading"] else "")

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("Robert Bowne Foundation"),  # donor
                mysql_quote(row["donee"]),  # donee
                str(amount),  # amount
                mysql_quote(row["year"] + "-01-01"),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote("Education/youth literacy"),  # cause_area
                mysql_quote("https://www.robertbownefoundation.org/grants.php"),  # url
                mysql_quote(notes),  # notes
            ]) + ")")
            first = False
        print(";")


def mysql_quote(x):
    """Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    our input is fixed and from a basically trustable source."""
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


if __name__ == "__main__":
    main()

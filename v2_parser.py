
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub
import csv

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):

    all_tables = {}
    all_tables['Bid'] = []
    all_tables['Categories'] = []
    all_tables['Items'] = []
    all_tables['Users'] = []
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # required fields
            itemid = int(item['ItemID'])
            name = item['Name'].replace('"', '""')
            currently = float(transformDollar(item['Currently']))
            first_bid = float(transformDollar(item['First_Bid']))
            number_of_bids = int(item['Number_of_Bids'])
            location = item['Location'].replace('"', '""')
            country = item['Country'].replace('"', '""')
            seller_id = item['Seller']['UserID'].replace('"', '""')
            rating = int(item['Seller']['Rating'])
            started = transformDttm(item['Started'])
            ends = transformDttm(item['Ends'])

            # categories are special b/c there can be multiple categories per item
            category_list = item['Category']

            # we add a special table for categories
            for cat in category_list:
                all_tables['Categories'].append([itemid, cat.replace('"', '""')])

            # not required fields

            # it says Description is required for each item, 
            #  but there is an instance where it is None
            if not item['Description']:
                description = "NULL"
            else:
                description = item['Description'].replace('"', '""')

            if 'Buy_Price' in item.keys():
                buy_price = float(transformDollar(item['Buy_Price']))
            else:
                buy_price = 'NULL'

            item_row = [itemid, seller_id, number_of_bids,
                    started, ends, first_bid, currently, name, 
                    description, buy_price ]
            all_tables['Items'].append(item_row)

            user_row = [ seller_id, rating, location, country]
            all_tables['Users'].append(user_row)

            # go through the bids to identify new users (who are not selling)
            #  and create rows for the Bid table
            if number_of_bids > 0:
                for bid in item['Bids']:
                    bidder = bid['Bid']['Bidder']
                    b_userid = bidder['UserID'].replace('"', '""')
                    b_rating = int(bidder['Rating'])
                    if 'Location' in bidder.keys():
                        b_location = bidder['Location'].replace('"', '""')
                    else:
                        b_location = 'NULL'
                    if 'Country' in bidder.keys():
                        b_country = bidder['Country'].replace('"', '""')
                    else:
                        b_country = 'NULL'

                    # update the Users table with a user making a bid
                    user_row = [ b_userid, b_rating, b_location, b_country ]
                    all_tables['Users'].append(user_row)

                    # update the Bid table
                    time = transformDttm(bid['Bid']['Time'])
                    amount = float(transformDollar(bid['Bid']['Amount']))

                    bid_row = [ b_userid, itemid, amount, time ]
                    all_tables['Bid'].append(bid_row)

    return all_tables 

def save_data(all_tables):

    tab_names = ['Bid', 'Categories', 'Items', 'Users']
    f_name = {}
    for name in tab_names:
        f_name[name] = f"_{name}.dat" 

    csv.register_dialect('formatting', delimiter=columnSeparator, quotechar='"',
                quoting=csv.QUOTE_NONNUMERIC, doublequote=True)

    for name in tab_names:

        with open(f_name[name], 'a', newline='') as f:
            csv_writer = csv.writer(f, 'formatting')
            for row in all_tables[name]:
                csv_writer.writerow(row)

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>', file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            all_tables = parseJson(f)
            save_data(all_tables)
            print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)

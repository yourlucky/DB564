#! /bin/bash

ARG1="-h"
if [ "$1" = "$ARG1" ]
then
	echo "NAME"
	echo -e "\tRuns a parser that goes through all 'items-*.json' files in the 'ebay_data' directory."
	echo -e "\tRows are sorted and duplicate tuples are removed."
	echo "DESCRIPTION"
	echo -e "\t./runParser.sh [-h]"
	echo "FLAGS"
	echo -e "\t[-h] displays this help menu"
	echo "OUTPUT"
	# comment out these lines if using awesome_parser.py
	echo -e "\tFour .dat files: Bid.dat, Categories.dat, Items.dat, and User.dat."
	echo -e "\tBid.dat file format:"
	echo -e "\t\tUser_ID|Item_ID|Amount|Time"
	echo -e "\tCategories.dat file format:"
	echo -e "\t\tItem_ID|Category"
	echo -e "\tItems.dat file format:"
	echo -e "\t\tItem_ID|User_ID|Number_of_bids|Started|Ends|First_Bid|Currently|Name|Description|Buy_Price"
	echo -e "\tUser.dat file format:"
	echo -e "\t\tUser_ID|Rating|Location|Country"

	# uncomment these for the awesome_parser.py
	#echo -e "\tThree .dat files: Bid.dat, Items.dat, and User.dat."
	#echo -e "\tBid dat file format:"
	#echo -e "\t\tUser_ID|Item_ID|Amount|Time"
	#echo -e "\tItems dat file format:"
	#echo -e "\t\tItem_ID|User_ID|Number_of_bids|Started|Ends|First_Bid|Currently|Name|Description|Buy_Price|"
	#echo -e "\t\t\tCategory_1|Category_2|Category_3|Category_4|Category_5|Category_6|Category_7|Category_8"
	#echo -e "\tUser dat file format:"
	#echo -e "\t\tUser_ID|Rating|Location|Country"

	echo ""
	echo "IMPORTANT NOTE: this script deletes all existing .dat files in the current directory"
else
	rm -f *.dat

	# comment out this line to run awesome_parser.py
	python3 v2_parser.py ebay_data/items-*.json

	# uncomment this line to run awesome_parser.py
	#python3 awesome_parser.py ebay_data/items-*.json

	cat _Bid.dat | sort | uniq > Bid.dat
	rm -f _Bid.dat

	cat _Items.dat | sort | uniq > Items.dat
	rm -f _Items.dat

	cat _Users.dat | sort | uniq > Users.dat
	rm -f _Users.dat

	# comment these two lines out if using awesome_parser.py
	cat _Categories.dat | sort | uniq > Categories.dat
	rm -f _Categories.dat
fi

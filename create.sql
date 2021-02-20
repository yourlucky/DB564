CREATE TABLE IF NOT EXISTS Users (
User_ID VARCHAR(30) PRIMARY KEY,
Rating INTEGER,
Location TEXT(300),
Country VARCHAR(20));


CREATE TABLE IF NOT EXISTS Items (
Item_ID INTEGER PRIMARY KEY,
User_ID VARCHAR(30),
Number_of_bids INT(3),
Started timestamp,
End timestamp,
First_Bid REAL,
Currently REAL,
Name VARCHAR(100),
Description TEXT,
Category_1 VARCHAR(200),
Category_2 VARCHAR(200),
Category_3 VARCHAR(200),
Category_4 VARCHAR(200),
Category_5 VARCHAR(200),
Category_6 VARCHAR(200),
Category_7 VARCHAR(200),
Category_8 VARCHAR(200),
FOREIGN KEY (User_ID) REFERENCES Users (User_ID)
);


CREATE TABLE IF NOT EXISTS Bid (
User_ID VARCHAR(30),
Item_ID INTEGER,
Amount Decimal(12,2),
Time timestamp,
PRIMARY KEY (User_ID, Item_ID),
FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
FOREIGN KEY (Item_ID) REFERENCES Items(Item_ID)
);

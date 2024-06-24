TRUNCATE Classes;
LOAD DATA INFILE '/home/josh/Documents/Visual Studio/Python/NewSeatingChart'
INTO TABLE students.Classes 
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
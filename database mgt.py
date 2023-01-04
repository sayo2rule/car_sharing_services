# 1a.
# Create an SQLite database and import the data into a table named “CarSharing”.
# Import the sqlite3 and csv modules.
import sqlite3 as sq
import csv

# Create a connection to the SQLite database by calling the "connect()" function.
conn = sq.connect("CarSharing.db", isolation_level=None)

# Create a cursor object to execute the SQLite commands using the cursor() method of the connection object.
cur = conn.cursor()

# use execute() method of the cursor object to create a new table in the database.
cur.execute('''
CREATE TABLE CarSharing (
    id INTEGER PRIMARY KEY, 
    timestamp TIMESTAMP, 
    season TEXT, 
    holiday TEXT, 
    workingday TEXT, 
    weather TEXT, 
    temp REAL, 
    temp_feel REAL, 
    humidity REAL, 
    windspeed REAL, 
    demand REAL)
''')

# Open the csv file and perform some preprocessing techniques on the csv file.
with open("/Users/user/Documents/Keele AI & DS/CSC-40054 (Data Analytics and Databases)/Coursework/CarSharing.csv", "r") as file:

    # Use the csv reader to read the file.
    reader = csv.reader(file)

    # skip the header row.
    next(reader)

    # iterate over the rows.
    for row in reader:
        # insert data into the table CarSharing.
        cur.execute("INSERT INTO CarSharing VALUES (?,?,?,?,?,?,?,?,?,?,?)", row)

# 1b.
# Create a backup table and copy the whole table into it.

cur.execute('''
CREATE TABLE CarSharing_backup AS 
SELECT * 
FROM CarSharing
''')

# 2a.
# Add a column to the CarSharing table named "temp_category".
cur.execute("ALTER TABLE CarSharing ADD COLUMN temp_category TEXT(3)")

# 2b.
# Update the values in the temp_category.
cur.execute('''
    UPDATE CarSharing
    SET temp_category = (
        CASE
            WHEN temp_feel < 10 THEN 'Cold'
            WHEN temp_feel BETWEEN 10 AND 25 THEN 'Mild'
            ELSE 'Hot'
        END
    )
''')

# 3a.
# Create another table named "temperature" featuring temp, temp_feel and temp_category columns.

cur.execute('''
    CREATE TABLE temperature (
        temp REAL,
        temp_feel REAL,
        temp_category TEXT
    )
''')

# Select the temp, temp_feel, and temp_category columns from the CarSharing table and insert them
# into the temperature table.
cur.execute('''
    INSERT INTO temperature (temp, temp_feel, temp_category)
    SELECT temp, temp_feel, temp_category
    FROM CarSharing
''')

# 3b.
# Drop the temp and temp_feel columns from the CarSharing table using the executescript() method
# of the cursor object.
cur.executescript('''
BEGIN;

ALTER TABLE CarSharing 
DROP COLUMN temp;

ALTER TABLE CarSharing 
DROP COLUMN temp_feel;

COMMIT;
''')

# 4a.
# Find the distinct values of the weather column
cur.execute("SELECT DISTINCT weather FROM CarSharing")

# Fetch the result.
distinct_weather = cur.fetchall()

# Print the distinct values.
for row in distinct_weather:
    print(row[0])

# 4b.
# Assign a number to each weather value
weather_code = {}
for i, weather in enumerate(distinct_weather):
    weather_code[weather[0]] = i

# 4c.
# Add the weather_code column to the CarSharing table
cur.execute('''
ALTER TABLE CarSharing ADD COLUMN weather_code INTEGER;
''')

# Update the weather_code column based on the weather column
for weather, code in weather_code.items():
    cur.execute('''
    UPDATE CarSharing
    SET weather_code = ?
    WHERE weather = ?;
    ''', (code, weather))

# Query the top 5 rows from the CarSharing table to have an idea of how the table looks like
cur.execute('''
SELECT * 
FROM CarSharing 
LIMIT 5;
''')

# Fetch and print the data
rows = cur.fetchall()
for row in rows:
    print(row)

# Query the column information for the CarSharing table to confirm the newly added columns
cur.execute("PRAGMA table_info(CarSharing)")

# Fetch and print the column names
columns = cur.fetchall()
for column in columns:
    print(f"{column[0]}: {column[1]}: {column[2]}")

# 5a.
# Create the weather table
cur.execute('''
CREATE TABLE weather(
weather TEXT,
weather_code INTEGER
)''')

# 5b.
# Copy the weather and weather_code's data from the CarSharing table into the table weather
cur.execute('''
INSERT INTO weather (weather, weather_code)
SELECT weather, weather_code 
FROM CarSharing
''')

# 5c. Drop the weather column from the CarSharing table
cur.execute('''
ALTER TABLE CarSharing 
DROP COLUMN weather
''')

# Query the column information for the CarSharing table to confirm if the column "weather" has been dropped
cur.execute("PRAGMA table_info(CarSharing)")

# Fetch and print the column names
columns = cur.fetchall()
for column in columns:
    print(f"{column[0]}: {column[1]}: {column[2]}")

# 6a.
# Create the table named "time" with four columns
cur.execute('''
CREATE TABLE time(
    timestamp TIMESTAMP,
    hour INTEGER,
    weekday TEXT,
    month TEXT);
''')

# Insert rows into the table "time"
cur.execute('''
INSERT INTO time (timestamp, hour, weekday, month)
SELECT
    strftime('%Y-%m-%d %H:%M:%S', timestamp) as timestamp,
    strftime('%H', timestamp) as hour,
    CASE strftime('%w', timestamp)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday' 
    END as weekday,
    CASE strftime('%m', timestamp) 
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END as month
FROM CarSharing; 
''')

# Query the top 5 rows from the "time" table to have an idea of how the table looks like.
cur.execute('''
SELECT * 
FROM time 
LIMIT 5;
''')

# Fetch and print the data.
rows = cur.fetchall()
for row in rows:
    print(row)

# 7a.
# Find the date and time with the highest demand rate in 2017.
cur.execute('''
SELECT t.timestamp, c.demand
FROM time AS t
INNER JOIN CarSharing AS c 
ON t.timestamp = c.timestamp
WHERE strftime('%Y', t.timestamp) = '2017'
ORDER BY c.demand DESC
LIMIT 1;
''')

# Fetch and print the result.
result = cur.fetchone()
print(f"The date and time with the highest demand rate in 2017 was {result[0]} with a demand rate of {result[1]}.")

# 7b.
# Provide a table containing the name of the weekday, month and season
# in which we had the highest and lowest average demand rates throughout 2017.

# 7bi.
# For the highest average demand rate throughout 2017, write a query that to call the
# executescript() method on and assign it to a variable.
query_highest_demand2017 = '''
BEGIN;

CREATE TABLE highest_demand2017(
    weekday TEXT,
    month TEXT,
    season TEXT,
    avg_demand REAL
);

INSERT INTO highest_demand2017
SELECT 
    CASE strftime('%w', timestamp)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday' 
    END as weekday,
    CASE strftime('%m', timestamp) 
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END AS month,
    season,
    AVG(demand) AS avg_demand
FROM CarSharing
WHERE strftime('%Y', timestamp) = '2017'
GROUP BY weekday, month, season
ORDER BY avg_demand DESC
LIMIT 1;

COMMIT;
'''

# 7bii.
# For the lowest average demand rate throughout 2017, write a query that to call on the
# executescript() method and assign it to a variable it.
query_lowest_demand2017 = '''
BEGIN;

CREATE TABLE lowest_demand2017(
    weekday TEXT,
    month TEXT,
    season TEXT,
    avg_demand REAL
);

INSERT INTO lowest_demand2017
SELECT 
    CASE strftime('%w', timestamp)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday' 
    END as weekday,
    CASE strftime('%m', timestamp) 
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END AS month,
    season,
    avg(demand) as avg_demand
FROM CarSharing
WHERE strftime('%Y', timestamp) = '2017'
GROUP BY weekday, month, season
ORDER BY avg_demand ASC
LIMIT 1;

COMMIT;
'''

# 7biii.
# Perform the executescript() method on the variable assigned to the query in 7bi.
cur.executescript(query_highest_demand2017)

# Fetch and print the data.
cur.execute("SELECT * FROM highest_demand2017")
highest_demand2017 = cur.fetchall()
for row in highest_demand2017:
    print(row)

# 7biv.
# Perform the executescript() method on the variable assigned to the query in 7bii.
cur.executescript(query_lowest_demand2017)

# Fetch and print the data.
cur.execute("SELECT * FROM lowest_demand2017")
lowest_demand2017 = cur.fetchall()
for row in lowest_demand2017:
    print(row)

# 7ci.
# Give a table showing the avg demand rate on different hours of that weekday in 7biii when
# we have the highest demand rates throughout 2017.

# Firstly, fetch the weekday of the highest demand rate throughout 2017.
cur.execute("SELECT weekday FROM highest_demand2017")
highest_weekday = cur.fetchone()
for row in highest_weekday:
    print(row)

# Then, create the table to show the average demand rate for different hours of the weekday
cur.execute("""
CREATE TABLE hour_highest_demand AS
SELECT strftime('%H', timestamp) AS hour,
AVG(demand) AS avg_demand,
FROM CarSharing
WHERE strftime('%Y', timestamp) LIKE '2017%'
AND strftime('%w', timestamp) = ?
    WHEN '0' THEN 'Sunday'
    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'
    WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'
    WHEN '5' THEN 'Friday'
    WHEN '6' THEN 'Saturday'
GROUP BY hour
ORDER BY avg_demand DESC
""", highest_weekday,)

# Fetch and print the data in the table
cur.execute("SELECT * FROM hour_highest_demand")
hour_highest_demand = cur.fetchall()

for row in hour_highest_demand:
    hour = row[0]
    avg_demand = row[1]
    print(f"Hour: {hour}, Average Demand: {avg_demand}")

# 7cii.
# Give a table showing the avg demand rate on different hours of that weekday in 7biv when
# we have the lowest demand rates throughout 2017.

# Fetch the weekday of the lowest demand rate throughout 2017.
cur.execute("SELECT weekday FROM lowest_demand2017")
lowest_weekday = cur.fetchone()
for row in lowest_weekday:
    print(row)

# Then, create the table to show the average demand rate for different hours of the weekday
cur.execute("""
CREATE TABLE hour_lowest_demand AS
SELECT strftime('%H', timestamp) AS hour, 
AVG(demand) AS avg_demand
FROM CarSharing
WHERE strftime('%Y', timestamp) LIKE '2017%' 
AND strftime('%w', timestamp) = ?
    WHEN '0' THEN 'Sunday'
    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'
    WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'
    WHEN '5' THEN 'Friday'
    WHEN '6' THEN 'Saturday'
GROUP BY hour
ORDER BY avg_demand ASC
""", lowest_weekday,)

# Fetch and print the data in the table
cur.execute("SELECT * FROM hour_lowest_demand")
hour_lowest_demand = cur.fetchall()

for row in hour_lowest_demand:
    hour = row[0]
    avg_demand = row[1]
    print(f"Hour: {hour}, Average Demand: {avg_demand}")

# 7di.
# Nature and frequency (prevalence) of the weather condition in 2017 with reference to it
# being cold, mild or hot and also the various weather conditions

# 7dii.
# Table for average, highest and lowest wind speed for each month in 2017

# 7diii.
# Table for average, highest and lowest humidity for each month in 2017

# 7div.
# Create table showing the average demand rate for each cold, mild and hot weather in 2017
# sorted in descending order based on their average demand rates

# 7e.
# Create table showing the information in 7d for the month with the highest average demand rate
# in 2017 and compare it with other months
# sqlalchemy-challenge

## Climate Analysis and Exploration

Create a Jupyter Notebook file and import dependencies, including matplotlib.pyplot, pandas, datetime, and SQLAlchemy.

Use SQLAlchemy.create_engine to connect to the hawaii.sqlite database.

Use SQLAlchemy automap_base() to reflect the tables from the database into classes and save a reference to those classes called Station and Measurement.

Use SQLAlchemy.inspect to get the column names and object types for each table.

Create a session link to the database with the SQLAlchemy Session() function.

### Precipitation Analysis

Find the most recent date in the Measurement table with a session.query for func.max(Measurement.date) and save the result.

Convert the date to a datetime object with the datetime.datetime.strptime() function.

Calculate the date on year prior to the end of the dataset by subtracting datetime.timedelta(days=365) from the most recent date.

Perform a session query for the 'date' and 'prcp' columns from Measurement table, filtering for dates greater than or equal to the calculated start date.

Save the query results into a list with a list comprehension then use the list to form a Pandas dataframe.

Convert the dataframe's 'Data' column to datetime format with the appropriate function.

Set the 'Date' column as the index and sort the dataframe by 'Date'.

Use the Pandas plot() function to generate a plot of the precipiation values over time.

![Image of precipitation graph](https://github.com/kellnergp/sqlalchemy-challenge/blob/main/Images/precipitation.png?raw=true)

Finally, use the Pandas describe() function to print the summary statistics for the precipitation data.

### Station Analysis

Use a session query to determine the number of stations in the dataset by calling the 'station' column from the Station table, grouping by 'station', and using the count() function.

Create a query to find the most active station by calling Station.station and func.count(Measurement.id), joining the tables on 'station', grouping by 'station', and sorting by the func.count(), descending.

Save the top result's station.

Query func.min(), func.max(), and func.avg() for the 'tobs' column from the Measurement table, filtering for rows where the 'station' is equal to the saved station.

Using the start date from the previous section and the saved station from this section as filters, query 'tobs' data from the Measurement table.

Save the results of the query into a list with a list comprehension then use the list to generate a Pandas dataframe.

Use the Pandas plot().hist() function to create a graph of temperature frequency within the query results, using 12 bins.

![Image of temperature frequency table](https://github.com/kellnergp/sqlalchemy-challenge/blob/main/Images/tempFrequency.png?raw=true)

Close the session before continuing to the next section.

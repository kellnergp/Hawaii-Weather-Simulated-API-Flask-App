# import dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

## database setup
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

## flask setup
app = Flask(__name__)

## flask routes
# define home route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"-----------------<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start]/<br/>" 
        f"(/api/v1.0/YYYY-MM-DD/)<br/>"
        f"/api/v1.0/[start]/[end]<br/>" 
        f"(/api/v1.0/YYYY-MM-DD/YYYY-MM-DD)"
    )

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of precipitation values for the last 12 months of data"""
    # save the last date in the data
    recent_date_str = session.query(func.max(Measurement.date)).all()[0][0]
    
    # convert to datetime object
    recent_date = dt.datetime.strptime(recent_date_str, '%Y-%m-%d')
    
    # determine date 1 year prior
    start_date = recent_date - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    
    # Convert the query results to a dictionary using date as the key and prcp as the value
    prcp_dict = {}
    
    for result in prcp_results:
        prcp_dict[result[0]] = result[1]
    
    # close session
    session.close()
    
    # return JSON dictionary
    return jsonify(prcp_dict)

# define stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset"""
    # query station identifiers and names from the table
    station_results = session.query(Station.station, Station.name)
    
    # generate list of all stations
    station_list = [{'Station ID':'Station Name'}]
    
    for  station, name in station_results:
        stat_dict = {station:name}
        
        if stat_dict not in station_list:
            station_list.append(stat_dict)
            
    # close session
    session.close()
    
    # return JSON list of stations
    return jsonify(station_list)

# set up tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Query the dates and temperature observations of the most active station for the last year of data"""
    # save the last date in the data
    recent_date_str = session.query(func.max(Measurement.date)).all()[0][0]
    
    # convert to datetime object
    recent_date = dt.datetime.strptime(recent_date_str, '%Y-%m-%d')
    
    # determine date 1 year prior
    start_date = recent_date - dt.timedelta(days=365)
    
    # List the stations and the counts of rows of data in descending order.
    s_list = session.query(Station.station, func.count(Measurement.id)).join(Measurement, Measurement.station==Station.station)\
                            .group_by(Station.station).order_by(func.count(Station.id).desc()).all()
    
    # save value of most active station id
    active_station = s_list[0][0]
    
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date)\
                                            .filter(Measurement.station == active_station)\
                                            .order_by(Measurement.date)
    
    # save list of temperature observations (TOBS) for the previous year
    tobs_list = [{'Date':'Temperature'}]
    
    for result in tobs_results:
        tobs_dict = {result[0]:result[1]}
        tobs_list.append(tobs_dict)
    
    # close session
    session.close()
    
    #return JSON list of tobs values
    return jsonify(tobs_list)

# set up start temperature route
@app.route("/api/v1.0/<start>/")

# set up start/end temperature route
@app.route("/api/v1.0/<start>/<end>")
def temp(start, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # conditional if an end is input
    if end != None:
        # convert inputs to datetime objects
        s_date = dt.datetime.strptime(start, '%Y-%m-%d')
        e_date = dt.datetime.strptime(end, '%Y-%m-%d')
        
        # query TMIN, TAVG, and TMAX for dates between the start and end date inclusive
        temp_results = session.query(func.min(Measurement.tobs),\
                       func.avg(Measurement.tobs),\
                       func.max(Measurement.tobs))\
                        .filter(Measurement.date >= s_date).filter(Measurement.date <= e_date)
    
    # if there is no end input
    else:
        # convert start to datetime object
        s_date = dt.datetime.strptime(start, '%Y-%m-%d')
        
        # query TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
        temp_results = session.query(func.min(Measurement.tobs),\
                       func.avg(Measurement.tobs),\
                       func.max(Measurement.tobs))\
                        .filter(Measurement.date >= s_date)
    
    # store results in list
    temp_list = [{'TMIN':temp_results[0][0]}, {'TAVG':temp_results[0][1]}, {'TMAX':temp_results[0][2]}] 
    
    # close session
    session.close()
    
    # return JSON list of temp results
    return jsonify(temp_list)

if __name__ == "__main__":
    app.run(debug=True)

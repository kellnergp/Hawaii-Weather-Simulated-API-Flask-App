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
Station = Base.classes.measurement

## flask setup
app = Flask(__name__)

## flask routes
# define home route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of precipitation values for the last 12 months of data"""
    # save the last date in the data
    recent_date = dt.datetime(2017, 8, 23)
    
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

    return jsonify(prcp_dict)

if __name__ == "__main__":
    app.run(debug=True)

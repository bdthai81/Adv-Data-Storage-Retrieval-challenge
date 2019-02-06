import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"

    )

@app.route("/api/v1.0/precipitations")
def precipitations():
    """Query for the dates and temperature observations from the last year.
       Convert the query results to a Dictionary using date as the key and tobs as the value.
       Return the JSON representation of your dictionary."""
    
    # Calculate the date 1 year ago from today (today being 2017-08-23)
    today = dt.date(2017, 8, 23)
    year_ago = today - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.prcp, Measurement.date)\
                                        .filter(Measurement.date >= year_ago)\
                                        .filter(Measurement.date < today).all()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for precipitation in results:
        precipitations_dict = {}
        precipitations_dict[precipitation.date] = precipitation.prcp
        all_precipitations.append(precipitations_dict)

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    # Perform a query to retrieve the stations
    results = session.query(Station.station).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station in results:
        stations_dict = {}
        stations_dict["station"] = station.station
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""

    # Calculate the date 1 year ago from today (today being 2017-08-23)
    today = dt.date(2017, 8, 23)
    year_ago = today - dt.timedelta(days=365)

    # Perform a query to retrieve the tobs from the previous year
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
                            .filter(Measurement.date >= year_ago)\
                            .filter(Measurement.date < today).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_tobs = []
    for tob in results:
        tobs_dict = {}
        tobs_dict["station"] = tob.station
        tobs_dict["date"] = tob.date
        tobs_dict["tobs"] = tob.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start, end=""):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    
    # Perform a query to calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.else:
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()
    # Create a dictionary from the row data and append to a list of all_stations
    all_mams = []
    for mam in results:
        mams_dict = {}
        mams_dict["TMIN"] = mam[0]
        mams_dict["TAVG"] = mam[1]
        mams_dict["TMAX"] = mam[2]
        all_mams.append(mams_dict)

    return jsonify(all_mams)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    
    # Perform a query to calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()
    
     # Create a dictionary from the row data and append to a list of all_stations
    all_mams = []
    for mam in results:
        mams_dict = {}
        mams_dict["TMIN"] = mam[0]
        mams_dict["TAVG"] = mam[1]
        mams_dict["TMAX"] = mam[2]
        all_mams.append(mams_dict)

    return jsonify(all_mams)

if __name__ == '__main__':
    app.run(debug=True)

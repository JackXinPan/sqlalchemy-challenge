import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect

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
        f"Precipitation of Last Year: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Observed Temperatures of Most active Station in Last Year: /api/v1.0/tobs<br/>"
        f"Input a start date at the end (yyyy-mm-dd) to find min, avg and max temperature up from then till now: /api/v1.0/<start><br/>"
        f"Input a start and end date at the end (yyyy-mm-dd) to find min, avg and max temperature between the dates: /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation values of last year of data\
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime( Measurement.date) >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation = []
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation list of station\
    results = session.query(Station.station).\
        group_by(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = []
    for station in results:
        station_id = station
        station_list.append(station_id)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query precipitation list of station\
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_count = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc())

    most_active = station_count.first()[0]

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == most_active).\
        filter(func.strftime( Measurement.date) >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    temperature_list = []
    for temp in results:
        temperature = temp
        temperature_list.append(temperature)

    return jsonify(temperature_list)
   
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query to find min, avg and max temperature
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)
    
    session.close
    temperature_list = []
    temperature_stats = {}
    for min, avg, max in results:
        temperature_stats["min"] = min
        temperature_stats["avg"] = avg
        temperature_stats["max"] = max
        temperature_list.append(temperature_stats)
    
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query to find min, avg and max temperature
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end)
    
    session.close
    temperature_list = []
    temperature_stats = {}
    for min, avg, max in results:
        temperature_stats["min"] = min
        temperature_stats["avg"] = avg
        temperature_stats["max"] = max
        temperature_list.append(temperature_stats)
    
    return jsonify(temperature_list)


if __name__ == '__main__':
    app.run(debug=True)
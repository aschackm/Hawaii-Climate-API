# Step 4-Climate App

#dependencies
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Connecting to and reflecting db
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

# Creating routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- Query for the dates and temperature observations from the last year<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- Return a JSON list of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- temperature observations from stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and precipitation observations from the last year"""
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_prior = datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_prior).order_by(Measurement.date).all()
    
    prcp_obs = []
    for obs in prcp:
        prcp_dict = {}
        prcp_dict["date"] = prcp[0]
        prcp_dict["prcp"] = prcp[1]
        prcp_obs.append(prcp_dict)

    return jsonify(prcp_obs)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name)
    
    station_list = []
    for s in stations:
        station_dict = {}
        station_dict["station"] = stations[0]
        station_dict["name"] = stations[1]
        station_list.append(station_dict)
        
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """temperature observations from stations"""
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_prior = datetime.strptime(recent_date, '%Y-%m-%d') - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > last_year).order_by(Measurement.date).all()
    
    tobs_list = []
    for s in stations:
        tobs_dict = {}
        tobs_dict["date"] = tobs[0]
        tobs_dict["tobs"] = tobs[1]
        tobs_list.append(station_dict)
        
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def trip1(start):
    """calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date"""
    start_date= datetime.strptime(start, '%Y-%m-%d')
    year_prior = dt.timedelta(days=365)
    start = start_date-year_prior
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    """calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive"""
    start_date= datetime.strptime(start, '%Y-%m-%d')
    end_date= datetime.strptime(end,'%Y-%m-%d')
    year_prior = dt.timedelta(days=365)
    start = start_date-year_prior
    end = end_date-year_prior
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == "__main__":
    app.run(debug=True)
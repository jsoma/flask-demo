from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'energy.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Plant(db.Model):
    __tablename__ = 'powerplants'
    
    plant_code = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String, nullable=False)
    utility_name = db.Column(db.String, nullable=False)
    utility_id = db.Column(db.Integer, nullable=False)
    sector_name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    county = db.Column(db.String, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    street_address = db.Column(db.String, nullable=False)
    primary_source = db.Column(db.String, nullable=False)
    total_mw = db.Column(db.Float, nullable=False)
    coal_mw = db.Column(db.Float, nullable=False)
    ng_mw = db.Column(db.Float, nullable=False)
    crude_mw = db.Column(db.Float, nullable=False)
    bio_mw = db.Column(db.Float, nullable=False)
    hydro_mw = db.Column(db.Float, nullable=False)
    nuclear_mw = db.Column(db.Float, nullable=False)
    solar_mw = db.Column(db.Float, nullable=False)
    wind_mw = db.Column(db.Float, nullable=False)
    geo_mw = db.Column(db.Float, nullable=False)
    other_mw = db.Column(db.Float, nullable=False)
    source_des = db.Column(db.String, nullable=False)
    tech_desc = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Plant {self.plant_name}>'

@app.route('/')
def list():
    # plants = Plant.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    plants = Plant.query.paginate(page=page, per_page=per_page)

    return render_template('list.html', plants=plants)

# Query for one power plant
@app.route('/plant/<plant_code>')
def plant(plant_code):
    plant = Plant.query.get(plant_code)

    return render_template('show.html', plant=plant)

# Query for one power plant
@app.route('/type/<primary_source>')
def by_source(primary_source):
    # Filter for the primary source
    plants = Plant.query.filter_by(primary_source=primary_source).all()

    plant_type = plants[0].primary_source

    return render_template('list.html', plants=plants, plant_type=plant_type)

# Query for one power plant
@app.route('/owner/<utility_id>')
def by_owner(utility_id):
    # Filter for the primary source
    plants = Plant.query.filter_by(utility_id=utility_id).all()
    owner_name = plants[0].utility_name

    return render_template('by_owner.html', plants=plants, owner_name=owner_name)

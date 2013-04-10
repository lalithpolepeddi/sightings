from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your-username:your-password@localhost/ufosightings'


class Sighting(db.Model):
  __tablename__ = 'sightings'
  id = db.Column(db.Integer, primary_key = True)
  sighted_at = db.Column(db.Integer)
  reported_at = db.Column(db.Integer)
  location = db.Column(db.String(100))
  shape = db.Column(db.String(10))
  duration = db.Column(db.String(10))
  description = db.Column(db.Text)
  lat = db.Column(db.Float(6))
  lng = db.Column(db.Float(6))


@app.route('/sightings/', methods=['GET'])
def sightings():
  if request.method == 'GET':
    lim = request.args.get('limit', 10)
    off = request.args.get('offset', 0)
    
    results = Sighting.query.limit(lim).offset(off).all()

    json_results = []
    for result in results:
      d = {'sighted_at': result.sighted_at,
           'reported_at': result.reported_at,
           'location': result.location,
           'shape': result.shape,
           'duration': result.duration,
           'description': result.description,
           'lat': result.lat,
           'lng': result.lng}
      json_results.append(d)

    return jsonify(items=json_results)

@app.route('/sightings/<int:sighting_id>', methods=['GET'])
def sighting(sighting_id):
  if request.method == 'GET':
    result = Sighting.query.filter_by(id=sighting_id).first()

    json_result = {'sighted_at': result.sighted_at,
                   'reported_at': result.reported_at,
                   'location': result.location,
                   'shape': result.shape,
                   'duration': result.duration,
                   'description': result.description,
                   'lat': result.lat,
                   'lng': result.lng}

    return jsonify(items=json_result)


if __name__ == '__main__':
  app.run(debug=True)

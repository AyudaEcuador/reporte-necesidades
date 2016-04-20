import requests
import json
import time
from flask import Flask, request, send_from_directory
from flask.ext.cors import CORS


app = Flask(__name__, static_url_path='')
app.debug = True
CORS(app)

@app.route('/<type>/<path:path>')
def send_static(type, path):
    return send_from_directory('static/{}'.format(type), path)

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/reporte', methods=['POST'])
def create_report():
    request_body = json.loads(request.data)
    title = request_body.get("incident_title")
    description = request_body.get("incident_description")
    category = request_body.get("incident_category")
    latitude = request_body.get("latitude")
    longitude = request_body.get("longitude")
    incident_date = time.strftime("%m/%d/%Y")
    incident_hour =  time.strftime("%I")
    incident_minute = time.strftime("%M")
    incident_ampm = time.strftime("%p").lower()
    location_name = request_body.get("location_name")

    response = add_report_to_platform('http://beta.mapa.desastre.ec/',
        incident_title=title,
        incident_description=description,
        incident_category=category,
        latitude=latitude,
        longitude=longitude,
        incident_date=incident_date,
        incident_hour=incident_hour,
        incident_minute=incident_minute,
        incident_ampm=incident_ampm,
        location_name=location_name)
    return json.dumps(response), 201

def add_report_to_platform(mapurl, **kwargs):
    pass
    if not kwargs.has_key('latitude'): kwargs['latitude'] = 0
    if not kwargs.has_key('longitude'): kwargs['longitude'] = 0
    if not kwargs.has_key('location_name'): kwargs['location_name'] = "unknown"
    payload = { 'task': 'report' }
    payload.update(kwargs)
    r = requests.post(mapurl + "api", data=payload)
    return r.text
    # return "Ok"

if __name__ == '__main__':
    app.run()

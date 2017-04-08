import requests
import geocoder
from flask import Flask, render_template, request

DEBUG = True
PORT = 2000
TEMPLATE_DIR = 'templates'
STATIC_DIR = 'static'

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

# handles raw conversion
@app.route('/w3w', methods=['GET', 'POST'])
def w3w():
	if request.method == 'POST':
		loc = request.form['q'].strip(" ")
		# latlng format
		latlng = loc.split(",")
		lat = latlng[0]
		lng = latlng[1]
		conn = requests.get("https://api.what3words.com/v2/reverse?coords=" + \
			lat + "%2C" + lng  +"&key=WVZ71D9D&lang=en& \
			format=json&display=full")
		what3words = conn.json()
		print(what3words)
		word = what3words['words']
		w3w_map = what3words['map']
		return render_template('w3w.html', lng=lng, lat=lat, word=word)
	return render_template('w3w.html')


# handles osm nominatim geocoder
@app.route('/geocoder_3words', methods=['GET', 'POST'])
def geocoder_words():
	if request.method == 'POST':
		# run a search on osm
		query = request.form['q']
		loc = geocoder.osm(query)
		dumps = loc.json
		lat = dumps['lat']
		lng = dumps['lng']
		address = dumps['address']

		# run conversion for what3words
		conn = requests.get("https://api.what3words.com/v2/reverse?coords=" + \
			str(lat) + "%2C" + str(lng)  +"&key=WVZ71D9D&lang=en& \
			format=json&display=full")
		what3words = conn.json()
		words = what3words['words']
		return render_template('osm_geocoder.html', address=address, lng=lng, lat=lat, words=words)
	return render_template('osm_geocoder.html')


if __name__ == "__main__":
	app.run()

import sqlite3

from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET"])
def index():

	state = request.args.get("state", default="") # get state variable from URL querystring
	storeNum = request.args.get("storeNum", default="") # get storeNum variable from URL querystring
	random = request.args.get("random", default="") # check if a request for random waffle house
	
	if storeNum != "": #display detailed information about a Waffle House Location

		with sqlite3.connect('wafflehouse.db') as conn:
			cursor = conn.cursor()
			cursor.execute("SELECT latitude, longitude, address, city, state FROM wafflehouse WHERE storeNum=?", [storeNum])
			location = (cursor.fetchone())
			
		return render_template("detail.html", location=location, storeNum=storeNum)

	elif random == "true": #get a random Waffle House
		
		with sqlite3.connect('wafflehouse.db') as conn:
			cursor = conn.cursor()
			cursor.execute("SELECT latitude, longitude, address, city, state FROM wafflehouse ORDER BY random() LIMIT 1")
			location = (cursor.fetchone())
			
		return render_template("random.html", location=location)
		
	elif request.args.get("state",default="") != "": # list Waffle House for a state
		state = request.args.get("state")

		with sqlite3.connect('wafflehouse.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT storeNum, name, address FROM wafflehouse WHERE state=?", [state])
			locations = (cursor.fetchall())
		
		return render_template("locations.html", locations=locations)

	else: # list a directory of Waffle House's by state
		
		with sqlite3.connect('wafflehouse.db') as conn:
			conn.row_factory = sqlite3.Row
			cursor = conn.cursor()
			cursor.execute("SELECT state, COUNT(*) FROM wafflehouse GROUP BY state ORDER BY COUNT(*) DESC")
			states = (cursor.fetchall())
		
		return render_template("index.html", states=states)


app.run(host='0.0.0.0', port=8080)
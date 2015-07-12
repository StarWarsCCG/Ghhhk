from flask import Flask, Response, json
from flask import request
import psycopg2
import json

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/card/<card>")
def card(card):
	try:
		val = int(card)
	except ValueError:
		return "Error, invalid card number"
	conn = psycopg2.connect("host=localhost dbname=swccg user=postgres password=guest222")
	cur = conn.cursor()
	cur.execute("select card_name from cards where id = (%s)", (card,))
	r = cur.fetchone()
	cur.close()
	conn.close()

	if r == None:
		return "No card found with that ID"
	else:
		return "<h2>{}".format(r[0]) + "</h2><img src=\"/static/images/c" + card + ".gif\">"

@app.route("/api/cards/search")
def search_by_title():
	# /api/cards/search_by_title
	# POST data -> 'title_search'
	# return a JSON doc of IDs and full card titles
	param = request.args.get('title')
	if param == None or param == "":
		return Response(json.dumps({}),  mimetype='application/json')

	search_string = '%' + param + '%'
	conn = psycopg2.connect("host=localhost dbname=swccg user=postgres password=guest222")
	cur = conn.cursor()
	cur.execute("select id, card_name from cards where card_name ILIKE (%s)", (search_string,))
	r = cur.fetchall()

	data = {}
	for row in r:
		data[row[0]] = row[1]
	output = json.dumps(data)

	cur.close()
	conn.close()
	
	return Response(output,  mimetype='application/json')

if __name__ == "__main__":
	app.run(debug=True)
	

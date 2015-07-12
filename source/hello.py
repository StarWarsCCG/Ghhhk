from flask import Flask
import psycopg2

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
		return "<h2>The card name is {}".format(r[0]) + "</h2><img src=\"/static/images/c" + card + ".gif\">"

if __name__ == "__main__":
	app.run(debug=True)
	

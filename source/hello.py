from flask import Flask, Response, json
from flask import request
import psycopg2
import json

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World!"

@app.route('/card/<card>')
def card(card):
	try:
		val = int(card)
	except ValueError:
		return 'Error, invalid card number'
	conn = psycopg2.connect('host=localhost dbname=swccg user=postgres password=guest')
	cur = conn.cursor()
	cur.execute('select card_name from cards where id = (%s)', (card,))
	r = cur.fetchone()
	cur.close()
	conn.close()

	if r == None:
		return 'No card found with that ID'
	else:
		return '<h2>{}'.format(r[0]) + '</h2><img src=\"/static/images/c' + card + '.gif\">'

@app.route('/api/cards/search')
def search_by_title():
	args = request.args
	# if param == None or param == '':
	conn = psycopg2.connect('host=localhost dbname=swccg user=postgres password=guest')
	cur = conn.cursor()

	query = 'select id, card_name from cards'
	param = ()
	conditions = []

	print('initial query: {}'.format(query))

	title = request.args.get('title')
	if title is not None:
		title = '%' + title + '%'
		conditions.append('card_name ILIKE (%s)')
		param += (title,)

	cardtype = request.args.get('cardtype')
	if cardtype is not None:
		cardtype = '%' + cardtype + '%'
		conditions.append('card_type ILIKE (%s)')
		param += (cardtype,)

	matching_weapon = request.args.get('match')
	if matching_weapon is not None:
		if matching_weapon == 'yes':
			conditions.append('matching_weapon IS NOT NULL')
		elif matching_weapon == 'no':
			conditions.append('matching_weapon IS NULL')
		else:
			pass

	grouping = request.args.get('grouping')
	if grouping is not None:
		if grouping == 'light':
			conditions.append('grouping = (%s)')
			param += ("Light",)
		elif grouping == 'dark':
			conditions.append('grouping = (%s)')
			param += ("Dark",)
		else:
			pass

	if not args == []:
		# build that query!
		query += ' where {}'.format(conditions[0])
		if len(conditions) > 1:
			for i in range(1,len(conditions)):
				query += ' and {}'.format(conditions[i])
	else:
		return Response(json.dumps({}),  mimetype='application/json')

	limit = request.args.get('limit')
	if limit is not None:
		try:
			val = int(limit)
		except ValueError:
			pass
		else:
			query += 'limit (%s)'
			param += (limit,)

	print('final query: {}'.format(query))

	cur.execute(query, param)
	r = cur.fetchall()

	data = {}
	for row in r:
		data[row[0]] = row[1]
	output = json.dumps(data)

	cur.close()
	conn.close()
	
	#set content-type to application/json, rather than text/html
	return Response(output,  mimetype='application/json')

if __name__ == "__main__":
	app.run(debug=True)
	
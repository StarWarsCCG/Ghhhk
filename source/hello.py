from flask import Flask, Response, json, request, make_response, redirect, render_template
from jinja2 import Environment, PackageLoader
import psycopg2
import datetime
import json

app = Flask(__name__)
env = Environment(loader=PackageLoader(__name__, 'templates'))

template = env.get_template('standard.html')

@app.errorhandler(404)
def page_not_found(e):
	template = env.get_template('404.html')
	return template.render(''), 404

def get_a_deck(deck_id):
	conn = psycopg2.connect('host=localhost dbname=swccg user=postgres password=guest')
	cur = conn.cursor()
	cur.execute('select id, name, date_created, is_light_side, description, date_modified, strategy, player_id, is_public from decks where id = (%s)', (deck_id,))
	r = cur.fetchone()
	cur.close()
	conn.close()

	# s = r[2].strftime('%B %-d, %Y @ %H:%M')

	data = {
		"id": int(r[0])
		,"name": str(r[1])
		,"date_created": r[2]
		,"is_light_side": r[3]
		,"description": str(r[4])
		,"date_modified": r[5]
		,"strategy": str(r[6])
		,"player_id": r[7]
		,"is_public": r[8]
	}
	
	return data



@app.route("/")
def hello():
	return template.render()

@app.route('/decks/new/dark')
def dark_deck_builder():
	template = env.get_template('deck_builder.html')
	return template.render()

@app.route('/test')
def test_template():
	template = env.get_template('test.html')
	return template.render(user='LordBuzzSaw')

@app.route('/card/<card_id>')
def card(card_id):
	try:
		val = int(card_id)
	except ValueError:
		return 'Error: invalid card number'
	conn = psycopg2.connect('host=localhost dbname=swccg user=postgres password=guest')
	cur = conn.cursor()
	cur.execute('select card_name from cards where id = (%s)', (card_id,))
	r = cur.fetchone()
	cur.close()
	conn.close()

	if r == None:
		template = env.get_template('404.html')
		return template.render(''), 404
	else:
		template = env.get_template('card.html')
		return template.render(name=r[0], card_id=card_id)

@app.route('/deck/<deck_id>')
def deck(deck_id):
	try:
		val = int(deck_id)
	except ValueError:
		return 'Error: invalid deck number'
	if deck_id is not None:
		try:
			val = int(deck_id)
		except ValueError:
			return 'Error: invalid deck number'
		else:
			deck = get_a_deck(deck_id)

			if deck["is_light_side"] is True:
				grouping = 'Light'
			else:
				grouping = 'Dark'

			if deck["is_public"] is True:
				privacy = 'Public'
			else:
				privacy = 'Private'

			template = env.get_template('deck.html')
			return template.render(
				deck_id=deck["id"]
				,name=deck["name"]
				,created=deck["date_created"].strftime('%B %-d, %Y @ %H:%M')
				,grouping=grouping
				,description=deck["description"]
				,modified=deck["date_modified"].strftime('%B %-d, %Y @ %H:%M')
				,player_id=deck["player_id"]
				,privacy=privacy
				,strategy=deck["strategy"]
			)



@app.route('/api/deck')
def api_deck_get():
	# deck_id = request.args.get('id')
	# try:
	# 	val = int(deck_id)
	# except ValueError:
	# 	return 'Error: invalid deck number'
	# if deck_id is not None:
	# 	try:
	# 		val = int(deck_id)
	# 	except ValueError:
	# 		return 'Error: invalid deck number'
	# 	else:
	# 		conn = psycopg2.connect('host=localhost dbname=swccg user=postgres password=guest')
	# 		cur = conn.cursor()

	# 		cur.execute('select id, name, date_created, is_light_side, description, date_modified, strategy, player_id, is_public from decks where id = (%s)', (deck_id,))
	# 		r = cur.fetchall()
			
	# 		cur.close()
	# 		conn.close()

	return 'yay'
	# return '{}'.format(r)

@app.route('/api/cards/search')
def api_cards_search():
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

@app.route('/snickerdoodle/set')
def set_snickerdoodle():
	resp = make_response(redirect('/snickerdoodle/get'))
	resp.set_cookie('username',value='success')
	return resp

@app.route('/snickerdoodle/set/<snicker>')
def set_snickerdoodle_custom(snicker):
	resp = make_response(redirect('/snickerdoodle/get'))
	resp.set_cookie('snicker',value=snicker)
	return resp

@app.route('/snickerdoodle/get')
def get_snickerdoodle():

	snicker = request.cookies.get('snicker')
	if snicker is None:
		return '<h4>Something is broken.</h4>'
	else:
		return '<h4>This doodle\'s snicker is {}.</h4>'.format(snicker)


if __name__ == "__main__":
	app.run(debug=True)
	

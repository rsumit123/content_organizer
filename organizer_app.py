
import io
import flask
import random
import json
import os
import copy
import numpy as np
import random

app = flask.Flask(__name__)
# content = json.loads(open('content.json').read())


@app.route('/')
def my_form():
	return flask.render_template('my_form.html')


@app.route('/delete')
def my_form_delete():
	return flask.render_template('my_form_delete.html')



##############################################################################
@app.route("/test", methods=["GET","POST"])
def test():
	data = {"status":200}
	return flask.jsonify(data)


@app.route("/random", methods=["GET"])
def get_random():
	with open('content.json','r') as w:
		content = json.load(w)
	ret = {"random":[]}
	rand = []
	for h in content:
		for sub_h in content[h]:
			rand.extend(content[h][sub_h])


	rand = random.sample(rand, 5)
	ret["random"]=rand
	return ret
	

@app.route("/head", methods=["GET"])
def get_headings_and_subheadings():
	with open('content.json','r') as w:
		content = json.load(w)

	result = {}
	for h in content:
		result[h]=list(content[h].keys())
	return result


@app.route("/display", methods=["GET"])
def display():
	with open('content.json','r') as w:
		content = json.load(w)
	return content

@app.route("/delete", methods=["POST"])
def delete():

	if flask.request.method == "POST":
		found = False
		with open('content.json','r') as w:
			content = json.load(w)
		content_copy = copy.deepcopy(content)
		heading = flask.request.form['heading'].strip().lower()
		sub = flask.request.form['sub'].strip().lower()
		date = flask.request.form['date'].strip().lower()
		body = flask.request.form['content'].strip()
		new_l = []
		for l in content[heading][sub]:
			if list(l.keys())[0]==date and list(l.values())[0]==body:
				found = True
			else:
				new_l.append({list(l.keys())[0]:list(l.values())[0]})


		content[heading][sub]=new_l
		if found == True:
			with open('./content.json','w') as fp:
				json.dump(content,fp)
			return {date:body,"status":"deleted"}
		else:
			return "Not found"

	
	

@app.route("/", methods=["POST"])
def predict():
	data = {"success": False}

	if flask.request.method == "POST":
		# if flask.request.files.get("image"):
			
		# image = flask.request.files["image"].read()
		# image = Image.open(io.BytesIO(image))

		# image = prepare_image(image, target=(224, 224))

		# text = flask.request.get_json(force=True)
		with open('content.json','r') as w:
			content = json.load(w)
		heading = flask.request.form['heading'].strip().lower()
		sub = flask.request.form['sub'].strip().lower()
		date = flask.request.form['date'].strip().lower()
		body = flask.request.form['content'].strip()


		if heading in content:
			if sub in content[heading]:
				content[heading][sub].append({date:body})
			else:
				content[heading][sub] = [{date:body}]
		else:
			content[heading] = {sub:[{date:body}]}
		
		with open('./content.json','w') as fp:
			json.dump(content,fp)

		data['success']= True
		


	return "content successfully saved in heading "+heading+"| subheading "+sub+"."

if __name__ == "__main__":
	print(("** Starting flask server..."
		"please wait until server has fully started"))
	
	app.run(host='0.0.0.0', port=5000,debug=True)

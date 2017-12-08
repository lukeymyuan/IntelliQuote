from flask import Flask, render_template, request
import Random_Forest
import json
app = Flask(__name__)
plan_model = None
premium_model = None

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/plans/<bronze>/<silver>/<gold>/<platinum>/")
def plans(bronze, silver, gold, platinum):
	return render_template("plans.html", bronze=bronze, silver=silver, gold=gold, platinum=	platinum)

@app.route("/forms")
def forms():
	return render_template("form.html")

@app.route("/forms2")
def forms2():
	return render_template("form2.html")

@app.route("/forms3")
def forms3():
	return render_template("form3.html")

@app.route("/form_submit", methods=['POST'])
def form_submit():
	print(request)
	the_dict = request.get_json(force=True, silent=True)
	months = dict(January=1, February=2, March=3,April=4, May=5, June=6, July=7, August=8, September=9, October=10, November=11, December=12)

	model_data = Random_Forest.Random_Forest(plan_model, premium_model, 0 if the_dict['gender'] == 'M' else 1, the_dict['date'].split(",")[1], months[the_dict['date'].split(' ')[1][:-1]], the_dict['smoke'], the_dict['income'], the_dict['optional_insured'], the_dict['weight'], the_dict['height'], the_dict['married'])

	print(model_data['platinum'][0])
	#return plans(model_data['bronze'][0], model_data['silver'][0], model_data['gold'][0], model_data['platinum'][0])

	'''
		{"plan": plan_prediction, "bronze": premiums["bronze"],
	            "silver": premiums["silver"], "gold": premiums["gold"],
	            "platinum": premiums["platinum"]}
	'''
	'''
		u'city': u'h3', u'first_name': u'abc', u'last_name': u'def', u'weight': u'3', u'gender': u'3',
		u'married': u'0', u'height': u'3', u'state': u'3', u'optional_insured': u'3', u'income': u'3',
		 u'smoke': u'1', u'address': u'hig', u'date': u'11 December, 2017'}
	'''
	return json.dumps({'bronze':model_data['bronze'][0],'silver':model_data['silver'][0],'gold':model_data['gold'][0],'platinum':model_data['platinum'][0]}), 200, {'ContentType':'application/json'}



if __name__ == "__main__":
	plan_model = Random_Forest.get_plan_model()
	premium_model = Random_Forest.get_premium_model()
	app.run(debug=True, host="0.0.0.0", port=8080)

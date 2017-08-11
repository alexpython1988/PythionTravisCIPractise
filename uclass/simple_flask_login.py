from flask import Flask, session, render_template, request, flash
# from pymongo import MongoClient
from flask_pymongo import PyMongo
# from MongoPractise import MongoPractise
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)
app.config['SESSION_TYPE'] = 'mongodb'
# app.config['TESTING'] = True
#for test
app.config['MONGO_URI'] = "mongodb://localhost:27017"
#for production
#app.config['MONGO_URI'] = "mongodb://localhost:27017/blog"
# app.config['MONGO2_DBNAME'] = 'blog'
mongo = PyMongo(app, config_prefix='MONGO')
# mp = MongoPractise()
# mp.connect_to_db('test')
# mp.create_collection('users')
# mp.single_insert("alex", "alex", "1234")
# client = MongoClient(app.config['DATABASE_URI'])
# db = client['blog']

# def create_app(dbn):
# 	app = Flask(__name__)
# 	# app.config.from_object(config)
# 	app.config['DEBUG'] = True
# 	app.secret_key = os.urandom(12)
# 	app.config['SESSION_TYPE'] = 'mongodb'
# 	app.config['TESTING'] = True
# 	db = MongoClient("localhost", 27017)[dbn]
# 	# db.init_app(app)
# 	return app, db

# def create_db(db_name):
# 	return MongoClient("localhost", 27017)[db_name]

# # app, db = create_app('blog')
# db = create_db('blog')	

@app.route('/')
def index():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return '''<h1 id='fail'>Hello Boss!</h1>
		 <a href='/logout'>Logout</a>'''

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route("/login", methods=['POST'])
def login():
	uname = request.form['username']
	upwd = request.form['password']

	if mongo.db.users.find_one({'_id': uname}) is not None:
		if mongo.db.users.find_one({'password': upwd}) is not None:
			session['logged_in'] = True
		else:
			flash('password is not correct.')
	else:
		flash('User not exist!')

	return index()

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	session['logged_in'] = False
	if request.method == 'POST':
		uname = request.form['username']
		upwd = request.form['password']

		if mongo.db.users.find_one({"_id": uname}) is None:
			d = dict()
			d["_id"] = uname
			d["password"] = upwd 
			mongo.db.users.insert_one(d)
			return index()
		else:
			flash("user already exist!")

	return render_template('signup.html')

if __name__=='__main__':
	app.run(host="127.0.0.1", port=19888)
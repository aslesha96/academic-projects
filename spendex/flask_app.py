from flask import *
from flask_sqlalchemy import *
import datetime
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key = 'random string'
db = SQLAlchemy(app)
activity_name=''
xyz='b'
# =================================================================================
class Users(db.Model):
	__tablename__='users'
	password = db.Column(db.String(255))
	email = db.Column(db.String(255),primary_key=True)
	def __init__(self,password,email):
		self.password=password
		self.email = email
	def __repr__(self):
		return '<Entry %r %r>' % (self.password, self.email)

class activities(db.Model):
	serial = db.Column(db.Integer, primary_key=True)
	activity_names=db.Column(db.String(255))
	admin_id=db.Column(db.String(255))
	participant_id=db.Column(db.String(255))
	paid = db.Column(db.Integer)
	Due = db.Column(db.Integer)
	pay=db.Column(db.Integer)
class data_transaction(db.Model):
	serial = db.Column(db.Integer, primary_key=True)
	activity_name=db.Column(db.String(255))
	buyer_email=db.Column(db.String(255))
	product=db.Column(db.String(255))
	price=db.Column(db.Integer)

class comment_section(db.Model):
	serial = db.Column(db.Integer, primary_key=True)
	activity=db.Column(db.String(255))
	participant_id=db.Column(db.String(255))
	comments=db.Column(db.String(255))
db.create_all()
# =================================================================================
@app.route("/chat",methods = ['GET','POST'])
def chat():
	global activity_name
	print("i entered chat")
	# d= db.session.query(chat).filter_by(activity_name=activity_name).all()
	print("blah***************************************************")
	# print(d)
	transac=db.session.query(data_transaction).filter_by(activity_name=activity_name).all()
	if request.method =='POST':
		print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
		p=session['email']
		c= request.form['comment']
		print(p)
		print("wwsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
		print(c)
		print(activity_name)
		if (whether_activitiesvalid(p,activity_name)):
			print("/////////////////////")
			msg=comment_section(activity=activity_name,participant_id=p,comments=c)
			print("#######################################################")
			db.session.add(msg)
			db.session.commit()
			print("*******************************************************")
		da=db.session.query(comment_section).filter_by(activity=activity_name).all()
		print(da)
		return render_template("transactions.html",error=" ",transac=transac,taskname='',comment=da)
	else:
		print("else request")
		return render_template("transactions.html",error=" ",transac=transac,taskname='',comment=da)

#==================================================================================
@app.route("/register",methods = ['GET','POST'])
def register():
	if request.method =='POST':
		password = request.form['password']
		Cpassword= request.form['cpassword']
		email = request.form['email']
		if(password==Cpassword):
			try:
				user = Users(password=password,email=email)
				db.session.add(user)
				db.session.commit()
				msg="Registered Successfully"
				return render_template("login.html",error=msg)
			except:
				db.session.rollback()
				msg="ACCOUNT ALREADY EXIST"
				db.session.close()
				return render_template("register.html",error=msg)
		else:
			msg="Password and confirm password does not match"
			return render_template("register.html",error=msg)

# =================================================================================

@app.route("/")
@app.route("/loginForm")
def loginForm():
	return render_template('login.html', error='')

# =================================================================================

@app.route("/Createaccount")
def registrationForm():
    return render_template("register.html",error='')

# =================================================================================
@app.route("/createactivity",methods = ['POST', 'GET'])
def createactivity():
	global activity_name
	if request.method =='POST':
		activity_name= request.form['activity_name']
		activity=activities(activity_names=activity_name,admin_id=session['email'],participant_id=session['email'],paid=0,Due=0,pay=0)
		db.session.add(activity)
		db.session.commit()
		return render_template("createactivity.html",error='',activity_name=activity_name,name='')
	else:
		return render_template("createactivity.html",error='',activity_name='',name='')
# =================================================================================
@app.route("/ADDPARTICIPATE",methods = ['POST', 'GET'])
def ADDPARTICIPATE():
	global paid
	global Due
	error=None
	if request.method =='POST':
		mobile=request.form['mobile']
		email=request.form['email']
		if(whether_valid(email)):
			error=''
			if(email!=session['email'] and (not whether_activitiesvalid(email,activity_name))):
				activity=activities(activity_names=activity_name,admin_id=session['email'],participant_id=email,paid=0,Due=0,pay=0)
				db.session.add(activity)
				db.session.commit()
			else:
				error='User already exists'
				return render_template("addparticipates.html",error=error)
			return render_template("createactivity.html",error=error,activity_name=activity_name,name=email)
		else:
			error="User doesn't exists"
			return render_template("createactivity.html",error=error,activity_name=activity_name,name='')
	else:
		return render_template("createactivity.html",error='',activity_name=activity_name,name='')
# =================================================================================
@app.route("/HOME")
def HOME():
	global d
	d= db.session.query(activities).filter_by(participant_id=email).all()
	# print(d)
	return render_template('Activities.html',mail=session['email'],d=d)
#==================================================================================
@app.route("/addparticipates")
def addparticipates():
    return render_template("addparticipates.html",error='')
#==================================================================================
@app.route("/transaction/<taskname>",methods=['POST','GET'])
def transaction(taskname):
	global activity_name
	global error
	global xyz
	activity_name=taskname
	error=''
	xyz=taskname
	da=db.session.query(comment_section).filter_by(activity=activity_name).all()
	transac=db.session.query(data_transaction).filter_by(activity_name=taskname).all()
	if request.method == 'POST':
		print("**************************")
		print(taskname)
		error=None
		email=request.form['email']
		product=request.form['product']
		price=request.form['price']
		print(email)
		print(product)
		print(price)
		if(whether_activitiesvalid(email,taskname)):
			print("////////////////s")
			print(email)
			print(taskname)
			print(product)
			print(price)
			t=data_transaction(activity_name=taskname,buyer_email=email,product=product,price=price)
			db.session.add(t)
			db.session.commit()
			aa = activities.query.filter_by(activity_names=taskname, participant_id=email).first()
			print("======================")
			temp=aa.paid
			print(type(temp))
			price=(int(price))
			aa.paid=price+temp
			db.session.commit()
		else:
			error="User doesn't exist"
			#return render_template("transactions.html",error=error,transac=transac,taskname=taskname,comment=da)
	transac=db.session.query(data_transaction).filter_by(activity_name=taskname).all()
	return render_template("transactions.html",error=error,transac=transac,taskname=taskname,comment=da)
#===================================================================================

@app.route("/login", methods = ['POST', 'GET'])
def login():
	global login_flag
	global d
	global email
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if is_valid(email, password):
			session['email'] = email
			# data_activity = "SELECT activities.activity_names FROM activities where session['email']==activities.participant_id"
			# d = db.engine.execute(data_activity).fetchall()
			d= db.session.query(activities).filter_by(participant_id=email).all()
			print(d)
			return render_template('Activities.html',mail=session['email'],d=d)
		else:
			error = 'Invalid UserId / Password'
			return render_template('login.html', error=error)

# =================================================================================

def is_valid(email,password):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False

# ===================================================================================
def whether_valid(email):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email:
			return True
	return False
#===================================================================================
def whether_activitiesvalid(email,activity_name):
	stmt = "SELECT * FROM activities"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[3] == email and row[1]==activity_name:
			return True
	return False
# #===================================================================================
@app.route("/logout")
def logout():
	session.clear()
	return render_template('login.html', error='')
#===================================================================================
@app.route("/summary",methods = ['POST', 'GET'])
def summary():
	print("2222222222222222222")
	print(xyz)
	totalAmount=0
	credit=0
	DueAmount=0
	d={}
	stmt = "SELECT * FROM activities"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[1]==xyz:
			totalAmount+=row[4]
	print(totalAmount)
	c=db.session.query(activities).filter(activities.activity_names == xyz).count()
	print(c)
	if c>0:
		share=totalAmount/c
	else:
		share=totalAmount
	d=calculation(xyz,share)
	print("//////////////////")
	print(d)
	return render_template('summary.html',TotalAmountSpent=totalAmount, ShareAmount=share,d=d)
#===================================================================================
def calculation(activity,share):
	stmt = "SELECT * FROM activities"
	data = db.engine.execute(stmt).fetchall()
	global participant_id
	global AmountSpent
	global credit
	global DueAmount
	participant_id=""
	AmountSpent=0
	credit=0
	DueAmount=0
	diction={}
	flag=0
	Pay=0
	for row in data:
		print("55555555555555555555555")
		print(row[1])
		if row[1]==activity:
			participant_id=row[3]
			AmountSpent=row[4]
			credit=AmountSpent
			print("ifffffffffffffffffff")
			if(credit>share):
				DueAmount=credit-share
				Pay=0

			else:
				Pay=share-credit
				DueAmount=0
		if(not (participant_id=='' and AmountSpent==0 and DueAmount==0 and Pay==0)):
			diction[participant_id]=[participant_id,AmountSpent,DueAmount,Pay]
		print("end of for loop")
	print(diction)
	return diction



if (__name__ == "__main__"):
	app.run()

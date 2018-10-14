import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash,json,jsonify,escape
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import Table
import json
from random import randint
app = Flask(__name__) # create the application instance :)
app.secret_key = 'any random string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db=SQLAlchemy(app)
with open("books.json") as data_file:
    data1 = json.loads(data_file.read())
class Cartproducts(db.Model):
    # __tablename__ = 'users'
    serial = db.Column(db.Integer, primary_key=True)  
    bookid =db.Column(db.String(80))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)
    title=db.Column(db.String(80))

    def __init__(self,bookid, quantity, price,title):
        self.bookid=bookid
        self.quantity = quantity
        self.price = price
        self.title=title

    def __repr__(self):
        return '<Entry %r %r %r %r>' % (self.bookid, self.quantity, self.price,self.title)

        
class Cart_user(db.Model):
    # __tablename__ = 'users'
    serial = db.Column(db.Integer, primary_key=True) 
    name=db.Column(db.String(80)) 
    phonenumber=db.Column(db.Integer)
    bookid =db.Column(db.String(80))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)
    title=db.Column(db.String(80))

    def __init__(self,name,phonenumber,bookid, quantity, price,title):
        self.name=name
        self.phonenumber=phonenumber
        self.bookid=bookid
        self.quantity = quantity
        self.price = price
        self.title=title

    def __repr__(self):
        return '<Entry %r %r %r %r %r >' % (self.name,self.phonenumber, self.quantity, self.price,self.title)

        

db.create_all() 


@app.route('/')
def index():
  print("---------------------index-fcf-------------------")
  return render_template('logout.html')


@app.route('/project')
def project():
	return render_template('Books.html')

@app.route('/placeorder',methods=['GET','POST'])
def palceorder():
  if request.method=='POST':
    name = request.form.get('name')
    phonenumber=int(request.form.get('phonenum'))
    print("=====================================")
    print(name)
    print(phonenumber)
    orders=Cartproducts.query.all()
    for z in orders:
      d=Cart_user(name=name,phonenumber=phonenumber,bookid=z.bookid,quantity=z.quantity,price=z.price,title=z.title)
      db.session.add(d)
      db.session.commit()
    for z in orders:
      db.session.delete(z)
      db.session.commit()
  return render_template('placedorder.html')


@app.route('/showorder',methods=['GET','POST'])
def showorder():
  if request.method=='POST':
    a=request.form.get('name')
    b=int(request.form.get('phonenum'))
    users=Cart_user.query.all()
    details= db.session.query(Cart_user).filter_by(name = a).filter_by(phonenumber = b).all()
    print(details)
    if len(details)==0:
      error="No data found"
      output=""
      output+='<h1>'+error+'</h1>'
      return output
    else:
      total=0
      for j in details:
        k=float(j.price)
        total=total+(k*j.quantity)
      total=total*(10/100)
      return render_template('details.html',details=details,total=total)


@app.route('/checkout')
def checkout():
  print(dicts)
  print(dicts2)
  ii=1
  total=0.0
  print(session)
  for x in session:
    print(x)
    q=session[x]
    z=dicts[x]
    print("***********************************")
    w=dicts2[x]
    print(str(ii)+": "+ str(x)+"  :  "+ str(q)+" : "+ str(z)+"  :  "+ str(w))
    d=Cartproducts(bookid=x,quantity=q,price=z,title=w)
    db.session.add(d)
    db.session.commit()
  orders=Cartproducts.query.all()
  for i in orders:
    # print(i.bookid)
    k=float(i.price)
    total=total+(k*i.quantity)
  total=total*(10/100)
  print("kishore")
  print(session)
  print(dicts)
  print(dicts2)
  return render_template('order.html',data1=data1,orders=orders,total=total,a=session,a1=dicts,a2=dicts2)


@app.route('/loadfile')
def loadfile():
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "problem-solving-books.json")
	data = json.load(open(json_url))
	return jsonify(data)

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#    if request.method == 'POST':
#       session['username'] = request.form['username']
#       return redirect(url_for('index'))
#    return '''
	
#    <form action = "/login" method = "post">
#       <p><input type = "text" name = 'username'/></p>
#         <input type="submit">
# </form>
	
#    '''

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   # session.pop('username',None)
   session.clear()
   print("**********************session is cleared**********************")
   return redirect(url_for('index'))

dicts={}
dicts2={}
@app.route('/<bid>/<price>/<title>')
def addtocart(bid,price,title):
  s=0
  flag=5
  # global prise
  # p=int(price)

  print("------------------------------------")
  print("bid:" + str(bid)+", "+ "price:" + str(price)+", title: "+str(title))
  print(type(price))
  if bid not in session:
       session[bid]=1
       dicts[bid]=(price)
       dicts2[bid]=(title)
  else:
    if(session[bid]<3):
        session[bid]=session[bid]+1
        # dicts[bid]=(price)
        # dicts2[bid]=(title)
    else:
      flag=6
  print(session)
  for x in session:
    s=s+session.get(x)
    print(s)

  a={
  "s":s,
  "flag":flag,
  "bid":bid,
  "price":price

  }


  return jsonify(a)

if __name__ == '__main__':
	app.run(debug=True)
	# session['username'] = 'admin'


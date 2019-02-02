from flask import Flask
from flask import render_template
from flask import *
import mysql.connector

app = Flask(__name__)
@app.route('/')
def about() :
    c = session.get('userid')
    return render_template('homepage.html',  c=c)
@app.route('/cart')
def cart() :
	uid = session.get('userid')
	if uid==None:
		session.clear()
		return render_template('homepage.html',msg='plz login or signup before adding products to cart',c=None)
	cart = session.get('cart')
	if cart==None:
		cart=dict()
	else:
		pass
	pid=request.args.get('pid')	
	price=request.args.get('price')	
	cart[pid]=int(price)
	session['cart']=cart
	return render_template('men.html', msg='added item to cart')
    # return str(pid)
    #return render_template('cart.html',  pid=pid)
@app.route('/viewcart')
def viewcart() :
	cart = session.get('cart')
	if cart==None:
		return 'cart is empty'
	s=0
	q=0
	for (k,v) in cart.items():
		s=s+int(v)
		q=q+1
	return render_template('cart.html', cart=cart, total=s, q=q)
    # return str(pid)
    #return render_template('cart.html',  pid=pid)

@app.route('/login')
def login() :
    return render_template('login.html')
@app.route('/loginpro' , methods = ['POST'])
def loginpro() :
    c=request.form['email']
    d=request.form['psw']
    cnx = mysql.connector.connect(user='root', database='kaira')
    cursor = cnx.cursor()

    sel_customer1 = "select count(*) from customer where cusemail= %s and cuspassword=%s"

    sel_customer2 = (c,d)

    cursor.execute(sel_customer1, sel_customer2)
    r = cursor.fetchone()


    cursor.close()
    cnx.close()
    if r[0]== 1:
       session['userid']=c
       return redirect('/')
    else:
       return redirect('/login')
       
    #return render_template('signup.html')
@app.route('/logout')
def logout() :
     session.clear()
     return redirect('/')	 

@app.route('/signup')
def signup() :
    return render_template('signup.html')
@app.route('/signpro', methods=['POST'])
def signpro() :
    a=request.form['name']
    b=request.form['num']
    c=request.form['email']
    d=request.form['psw']
    cnx = mysql.connector.connect(user='root', database='kaira')
    cursor = cnx.cursor()

    add_customer = ("INSERT INTO customer "
               "(cusname, cusphone, cusemail,cuspassword) "
               "VALUES (%s, %s, %s,%s)")

    data_customer = (a,b,c,d)

    cursor.execute(add_customer, data_customer)

    cnx.commit()

    cursor.close()
    cnx.close()
    session['userid']=c
    return redirect('/')
    #return render_template('signup.html')
@app.route('/men')
def men() :
    return render_template('men.html')
@app.route('/checkout')
def checkout() :
 
    return render_template('checkout.html')	
@app.route('/end' , methods = ['POST'])
def end() :
    a=request.form['address']
    b=request.form['cardname']
    c=request.form['cardnumber']
    d=request.form['expmonth']
    e=request.form['expyea']
    f=request.form['cvv']
    cnx = mysql.connector.connect(user='root', database='kaira')
    cursor = cnx.cursor()
    add_payment = ("INSERT INTO payment "
               "(address, cname, cnum, expm, expy, cvv,cusemail) "
               "VALUES (%s, %s, %s,%s,%s,%s,%s)")
    data_payment = (a,b,c,d,e,f,session.get('userid'))
    cursor.execute(add_payment, data_payment)
    cart=session['cart']
    for (k,v) in cart.items():
        add_orders = ("INSERT INTO orders (pid, cusemail, quantity,pprice) VALUES (%s, %s, %s,%s)")
        data_orders = (k,session.get('userid'),1,v)
        cursor.execute(add_orders, data_orders)
    cnx.commit()
    cursor.close()
    cnx.close()
    return render_template('end.html')	
	

	
app.secret_key = 'any random string'
app.run()

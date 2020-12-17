from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
import os
import sqlite3
from flask_mysqldb import MySQL

# Getting the current directory of the chatbot


currentDirectory = os.path.dirname(os.path.abspath(__file__))






app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbot'
mysql = MySQL(app)

msg = "Hello, world"
@app.route("/")
def hello():
    return "Working fine"

@app.route('/dashboard')
def backend():
	 cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', computers=rv)
	return render_template('index.html')


@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')

    # Create reply
    responded = False
    resp = MessagingResponse()

    delivery_message = ''
    ordering = False

    if 'Hi' in msg or 'hi' in msg:
    	delivery_message = "Hello, how are you? How I can help you today"
    	responded = True

    if 'Who are you' in msg:
    	delivery_message = "I'm a bot written in python to help you."
    	responded = True

    if 'what you can do' in msg:
    	delivery_message = "I can help you with all the information trained in me."
    	responded = True
    if "want to order" in msg or ordering:

    	customer_details = []
    	while(i<=7){

    	}
    
    if not responded:
    	delivery_message = "Hi, I didn't understand what you said"
    	responded = True


    resp.message(delivery_message)

    return str(resp)

@app.route('/simpan',methods=["POST"])
def simpan():
    title = request.form['title']
    description = request.form['description']
    orders = request.form['orders']
    price = request.form['price']
    category = request.form['category']
    image = request.form['image']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (`title`, `description`, `orders`, `price`, `category`, `image`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(title,description,orders,price,category,image,status,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/update', methods=["POST"])
def update():
    id_data = request.form['id']
    title = request.form['title']
    description = request.form['description']
    orders = request.form['orders']
    price = request.form['price']
    category = request.form['category']
    image = request.form['image']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE products SET title=%s, description=%s, orders=%s, price=%s, category=%s, image=%s, status=%s WHERE id=%s", (title,description,orders,price,category,image,status,id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))

@app.route('/about-us')
def about():
    return render_template('about-us.html')

@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')


if __name__ == "__main__":
    app.run(debug=True)
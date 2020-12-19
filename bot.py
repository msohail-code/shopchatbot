from flask import Flask, request, render_template, url_for, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

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
    return redirect(url_for('home'))

@app.route('/dashboard')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    cur.close()
    return render_template('home.html', computers=rv)

@app.route("/sms", methods=['POST'])
def sms_reply():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    from_ = request.form.get('From')

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
    
    if "show products" in msg or "Show products" in msg:
        
        for row in rv:
           delivery_message = delivery_message+ row[1]+" = $"+ str(row[4]) + "\n"
        responded = True
    if 'want to order':
        print ("working")
    
    if not responded:
    	delivery_message = "Hi, I didn't understand what you said"
    	responded = True


    resp.message(delivery_message)
    print(request.form)
    cur.close()
    return str(resp)

@app.route('/simpan',methods=["POST"])
def simpan():
    title = request.form['title']
    description = request.form['description']
    orders = request.form['orders']
    price = request.form['price']
    category = request.form['category']
    imageMain = request.files['image']
    image = secure_filename(imageMain.filename)
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (`title`, `description`, `orders`, `price`, `category`, `image`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s)",(title,description,orders,price,category,image,status,))
    imageMain.save('static/images/'+image)
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
    imageMain = request.files['image']
    image = secure_filename(imageMain.filename)
    
    imagetmp = imageMain.mimetype
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE products SET title=%s, description=%s, orders=%s, price=%s, category=%s, image=%s, status=%s WHERE id=%s", (title,description,orders,price,category,image,status,id_data,))
    imageMain.save('static/images/'+image)
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

@app.route('/orders')
def orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    rv = cur.fetchall()
    cur.close()
    return render_template('orders.html', computers=rv)

@app.route('/checkout')
def checkout():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    rv = cur.fetchall()
    cur.close()
    return render_template('checkout.html', computers=rv)


@app.route('/confirm_order', methods=["GET","POST"])
def confirm_order():
    name = request.form['name']
    emarate = request.form['emarate']
    area = request.form['area']
    string_number = request.form['string_number']
    home_number = request.form['home_number']
    phone_number = request.form['phone_number']
    products = request.form['pid']
    print(products)
    price = request.form['total_price']
    products_id = ''   
    # for pid in products:
    #     products_id = products[pid]+","


    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `orders`(`pid`,`area`, `name`, `home_number`, `phone_number`, `total_price`,street_number,emerate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(products,area,name,home_number,phone_number,price,string_number,emarate))
    cur.execute("UPDATE products SET orders=orders+1 WHERE id=%s", (products))
    mysql.connection.commit()
    return redirect(url_for('checkout'))

if __name__ == "__main__":
    app.run(debug=True)
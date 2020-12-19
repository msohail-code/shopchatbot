from flask import Flask, request, render_template, url_for, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client 
import os
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

# Getting the current directory of the chatbot


currentDirectory = os.path.dirname(os.path.abspath(__file__))






app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'chatbot' # database name
mysql = MySQL(app)
account_sid = 'AC212913ecfcd499d33f93485c6953f402' # copied from twilio concole
auth_token = '6a67d928ddedf6247c3ef77d1fff3c9e' # copied from twilio concole
client = Client(account_sid, auth_token) 
msg = "Hello, world"
p_url = "https://9ae0637ef9fd.ngrok.io/"
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
   
    
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    from_ = request.form.get('From')

    # Create reply
    responded = False
    resp = MessagingResponse()

    delivery_message = ''
    ordering = False

    cur = mysql.connection.cursor()
    required_hint = "%"+msg+"%"
    cur.execute("SELECT * FROM chatbot where questions LIKE %s",(required_hint,))
    rv = cur.fetchall()
    cur.close()

    for row in rv:
        delivery_message = row[2]
        responded = True


   

    if "want to order" in msg:
        delivery_message = "Checkout: "+p_url+"checkout"
        responded = True
    	
    
    if "show products" in msg or "Show products" in msg:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM products")
        rv = cur.fetchall()
        if cur.rowcount>0:
            for row in rv:
               delivery_message = delivery_message+ row[1]+" = $"+ str(row[4]) + "\n"
            responded = True
        else:
            delivery_message ="No, products Right now"
        cur.close()
    if 'want to order':
        print ("working")
    
    if not responded:
    	delivery_message = "Hi, I didn't understand what you said"
    	responded = True


    resp.message(delivery_message)
    print(request.form)
    
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

@app.route('/insert_hint',methods=["POST"])
def insert_hint():
    title = request.form['title']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO chatbot (`questions`, `hint`) VALUES (%s,%s)",(title,description,))
    mysql.connection.commit()
    return redirect(url_for('chatbot'))


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

@app.route('/update_hint', methods=["POST"])
def update_hint():
    id_data = request.form['id']
    title = request.form['title']
    description = request.form['description']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE chatbot SET questions=%s, hint=%s WHERE id=%s", (title,description,id_data,))
    mysql.connection.commit()
    return redirect(url_for('chatbot'))

@app.route('/hapus/<string:id_data>', methods=["GET"])
def hapus(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('home'))


@app.route('/delete_hint/<string:id_data>', methods=["GET"])
def delete_hint(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM chatbot WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('chatbot'))


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
    price = 0
    products_id = ''   
    # for pid in products:
    #     products_id = products[pid]+","
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products where id=%s",(products,))
    rv = cur.fetchall()
    for row in rv:
        price = row[4] + (row[4]*0.2)
    cur.close()


    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `orders`(`pid`,`area`, `name`, `home_number`, `phone_number`, `total_price`,street_number,emerate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(products,area,name,home_number,phone_number,price,string_number,emarate))
    cur.execute("UPDATE products SET orders=orders+1 WHERE id=%s", (products))
    mysql.connection.commit()

    
     
    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body='Thanks for Order: ' +name +"\nYour total is: AED"+str(price) ,      
                                  to='whatsapp:+' +phone_number
                              ) 
    
    return render_template('confirm.html',c_name =name,c_price=price)
    
@app.route('/checksms')
def checksms():
    
    client = Client(account_sid, auth_token) 
     
    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body='Automated message',      
                                  to='whatsapp:+'+'923039731680' 
                              ) 
     
    return "working"

@app.route('/chatbot')
def chatbot():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM chatbot")
    rv = cur.fetchall()
    cur.close()
    return render_template('chatbot.html', computers=rv)

if __name__ == "__main__":
    app.run(debug=True)
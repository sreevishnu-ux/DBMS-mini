import os
from flask import Flask, render_template ,request, redirect, url_for,flash
import mysql.connector as mysql

mydb = mysql.connect(host="localhost" , user="root" , passwd="Hanx@1" , database="antivenom",auth_plugin="mysql_native_password")
cursor = mydb.cursor()
cursor.execute("Use antivenom;")

class person:
    person_id = 0
    app_id=0

prn = person()


app = Flask(__name__)



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/av_location")
def av_location():
    return render_template("av_location.html")

@app.route("/appointment")
def appointment():
    return render_template("appointment.html")

@app.route("/delete_appointment")
def delete_appointment():
    return render_template("delete_appointment.html")



@app.route("/delete_app",methods=['POST','GET'])
def delete_app():
    sql_Delete_query ="""DELETE  FROM appointment WHERE aid=%s"""
    aid=request.form.get('aid')
    cursor.execute(sql_Delete_query, (aid,))
    mydb.commit()
    return redirect(url_for('view_appointment_inserted'))

@app.route("/update_appointment")
def update_appointment():
    return render_template("update_appointment.html")
    
@app.route("/update_app",methods=['POST'])
def update_app():
    aid=request.form.get('aid')
    date_time=request.form.get('date_time')
    update_query="""UPDATE appointment SET date_time=%s WHERE aid=%s"""
    cursor.execute(update_query,(date_time,aid,))
    mydb.commit()
    return redirect(url_for('view_appointment_inserted'))

@app.route("/login_insert",methods=['POST'])
def login_insert():
    username=request.form.get('username')
    password=request.form.get('password')
    cursor.execute("""
    INSERT INTO login(username,password) VALUES(%s,%s)""",(username,password))
    mydb.commit()
    return render_template("index2.html") 


@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/contact")
def contact():
    cursor.execute("""SELECT Contact_no FROM AV_Centre """)
    emergency_contact=cursor.fetchall()
    return render_template("contact.html",con=emergency_contact)

    

#@app.route("/delete_appointment/<string:aid>",methods=['POST','GET'])
#def delete_appointment(aid):
 #   cursor.execute("""DELETE  FROM appointment WHERE appointment.aid=%s""",(aid,))
  #  return "Deleted successfully"


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add_facility",methods=['POST'])
def add_facility():
    Facility_ID = request.form.get('Facility_ID')
    Facility_Name = request.form.get('Facility_Name')
    City = request.form.get('City')
    District = request.form.get('District')
    State = request.form.get('State')
    Contact_no = request.form.get('Contact_no')
    AV_Name = request.form.get('AV_Name')
    Available_Qty = request.form.get('Available_Qty')
    AV_Price=request.form.get('AV_Price')
    cursor.execute("""
                INSERT INTO AV_Centre(Facility_ID,Facility_Name,City,District,State,Contact_no,AV_Name,Available_Qty,AV_Price) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (Facility_ID,Facility_Name,City,District,State,Contact_no,AV_Name,Available_Qty,AV_Price))
    mydb.commit()
    return redirect(url_for('view_registered'))


@app.route("/add_persons_button",methods=['POST'])
def add_persons_button():
    Pid  = request.form.get('Pid')
    prn.person_id = Pid
    Name  = request.form.get('Name')
    Age  = request.form.get('Age')
    City    = request.form.get('City')
    District  = request.form.get('District')
    State  = request.form.get('State')
    Snake_type  = request.form.get('Snake_type')
    Snake_colour  = request.form.get('Snake_colour')

    cursor.execute("""
                INSERT INTO Person(Pid,Name,Age,City,District,State,Snake_type,Snake_colour) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                """, (Pid,Name,Age,City,District,State,Snake_type,Snake_colour ))
    mydb.commit()
    return redirect(url_for('view_av_centres'))


@app.route("/view_registered")
def view_registered():
    cursor.execute("""SELECT Facility_ID,Facility_Name,City,District,State,Contact_no,AV_Name,Available_Qty,AV_Price FROM AV_Centre""")
    return render_template("reg_av_details.html", reg = cursor.fetchall())
    


@app.route("/view_av_centres")
def view_av_centres():
    cursor.execute("""SELECT Facility_ID,Facility_Name,City,District,State,Contact_no,AV_Name,Available_Qty,AV_Price FROM AV_Centre A  WHERE A.City IN (SELECT City FROM Person WHERE Pid=%s )  """, (prn.person_id, ))
    return render_template("av_details.html", av = cursor.fetchall())
    
@app.route("/insert_appointment",methods=['POST'])
def insert_appointment():
    aid=request.form.get('aid')
    docname=request.form.get('docname')
    phone=request.form.get('phone')
    date_time=request.form.get('date_time')
    Facility_ID=request.form.get('Facility_ID')
    cursor.execute("""
    INSERT INTO appointment(aid,docname,phone,date_time,Facility_ID) VALUES(%s,%s,%s,%s,%s)""", (aid,docname,phone,date_time,Facility_ID))
    mydb.commit()
    return redirect(url_for('view_appointment_inserted'))

@app.route("/view_appointment_inserted")
def view_appointment_inserted():
    cursor.execute("""SELECT aid,docname,phone,date_time,Facility_ID FROM appointment """)
    return render_template("appointment_inserted.html",app=cursor.fetchall())

@app.route("/place_order",methods=['POST','GET'])
def place_order():
    return render_template("orders.html")
        
        
@app.route("/Add_product")
def Add_product():
    return render_template("add_orders.html")
    
@app.route("/insert_order",methods=['POST'])
def insert_order():
    Order_ID=request.form.get('Order_ID')
    Cust_name=request.form.get('Cust_name')
    Product_ID=request.form.get('Product_ID')
    Product_Name=request.form.get('Product_Name')
    Price=request.form.get('Price')
    cursor.execute("""
    INSERT INTO orders(Order_ID,Cust_name,Product_ID,Product_Name,Price) VALUES(%s,%s,%s,%s,%s)""", (Order_ID,Cust_name,Product_ID,Product_Name,Price))
    mydb.commit()
    return redirect(url_for('view_orders_inserted'))

@app.route("/view_orders_inserted")
def view_orders_inserted():
    cursor.execute("""SELECT Order_ID,Cust_name,Product_ID,Product_Name,Price FROM orders """)
    return render_template("order_added.html",ord=cursor.fetchall())

    
@app.route("/Cancel_order")
def Cancel_order():
    return render_template("cancel_orders.html")
    
@app.route("/delete_order",methods=['POST','GET'])
def delete_order():
    sql_Cancel_query ="""DELETE  FROM orders WHERE Order_ID=%s AND Product_ID=%s"""
    Order_ID=request.form.get('Order_ID')
    Product_ID=request.form.get('Product_ID')
    cursor.execute(sql_Cancel_query, (Order_ID,Product_ID,))
    mydb.commit()
    return redirect(url_for('view_orders_inserted'))
    
@app.route("/Change_product")
def Change_product():
    return render_template("change_orders.html")

        
@app.route("/update_order",methods=['POST','GET'])
def update_order():
    Order_ID=request.form.get('Order_ID')
    Product_ID=request.form.get('Product_ID')
    Product_Name=request.form.get('Product_Name')
    Price=request.form.get('Price')
    update_query_orders="""
                        UPDATE orders SET Product_ID =  %s,Product_Name = %s,Price =  %s WHERE Order_ID = %s
                        """
    cursor.execute(update_query_orders,(Product_ID,Product_Name,Price,Order_ID))
    mydb.commit()
    return redirect(url_for('view_orders_inserted'))
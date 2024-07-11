from flask import Flask, render_template,request,redirect, url_for, session
import secrets
import json,datetime
import random


today = str(datetime.date.today())
usr_email  = ""
usr_name = ""
usr_tp = ""
user_type = ""
temp_id = ""
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# use_details = {"abc@gmail.com":"abc",'user2': 'password2', 'user3': 'password3'}



def genarateOTP():
    return random.randint(1000,9999)
@app.route("/signin",methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        # Retrieve username and password from the form submission
        username = request.form['email']
        password = request.form['password']
        

        # # Check if the submitted username exists and the password matches
        # if username in use_details and use_details[username] == password:
        #     # Store username in session to indicate user is logged in
        #     session['username'] = username
        #     return redirect(url_for('index'))
        # else:
        #     # If username or password is incorrect, show an error message
        #     return "Invalid username or password. Please try again."
        with open("user.json","r") as file:
            jason_file = json.load(file)
        keys = list(jason_file.keys())
        for i in keys:
            if i == username:
                session['username'] = username
                
                if jason_file.get(i)["password"]==password:
                    global usr_email
                    global usr_name
                    global usr_tp
                    global user_type
                    usr_email = i
                    usr_name = jason_file.get(i)["name"]
                    usr_tp = jason_file.get(i)["tp"]
                    user_type = jason_file.get(i)["usertype"]


                   


                    return redirect(url_for("index"))
                    
                    

    return render_template('signin.html')
@app.route('/')
def index():
    # Check if user is logged in (i.e., session contains username)
    if 'username' in session:
        return render_template('index.html')
    else:
    
        return redirect(url_for('signin'))
    return render_template('index.html')
    



@app.route("/registration",methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        # Retrieve username and password from the form submission
        username = request.form['username']
        password = request.form['password']
        tp = request.form['tp']
        user_type = request.form['usertype']

        # Check if the username already exists
        with open("user.json","r") as file:
            jason_file = json.load(file)
        keys = list(jason_file.keys())
        for i in keys:
            if i == username:
                return "Username already exists. Please choose a different username."
            else:
                jason_file[username] = {"password":password,"name":username,"tp":tp,"usertype":user_type}
                with open("user.json","w") as file:
                    json.dump(jason_file,file)
                return redirect(url_for('signin'))

@app.route('/profile')
def profile():
    # with open("user.json","r") as file:
    #     jason_file = json.load(file)
    #     filtered_data = {usr_email: user_data for id, user_data in jason_file.items() if usr_email == usr_email}
        # userType = filtered_data.get(usr_email).get("usertype")
    if(user_type=="food_buyers"):
        with open("buying_orders.json","r") as file:
            jason_file = json.load(file)
        filtered_data = {id: user_data for id, user_data in jason_file.items() if user_data["buyer_email"] == usr_email}
        return render_template('profile_for_food_buyers.html',user_email = usr_email,user_name = usr_name,user_type = user_type,tp = usr_tp,json_file = filtered_data )
    else:
        print("food_maker")
        with open("buying_orders.json","r") as file:
            jason_file = json.load(file)
        filtered_data = {id: user_data for id, user_data in jason_file.items() if user_data["sender_email"] == usr_email}
        return render_template('profile_for_food_makers.html',user_email = usr_email,user_name = usr_name,tp = usr_tp,user_type = user_type,json_file = filtered_data )
   
@app.route('/get_food_request',methods=['GET','POST'])
def get_food_request():
    if request.method == 'POST':
        random_number = random.randint(10000, 100000)

        global usr_email
        meal = request.form['meals']
        food_item = request.form["foodname"]
        veg_non_veg = request.form.get("veg_nonveg")
        quantity = int(request.form["quantity"])
        unit_price = int(request.form.get("unit_price"))
        phone_number = request.form["phoneno"]
        type = request.form.get("request_type")

        print(meal,food_item,quantity,phone_number,type)
        if(type == "availability"):
            with open("food_availability.json","r") as file:
                jason_file = json.load(file)
            new_data = {random_number:{"email":usr_email,"category":meal,"phone":phone_number,"date":today,"status":'',"foodname":food_item,"foodquantity":quantity,"foodprice":unit_price,"totalprice":unit_price*quantity,"OTP":""}}
            jason_file.update(new_data)
            with open("food_availability.json","w") as file:
                json.dump(jason_file,file)
        else:
            with open("food_request.json","r") as file:
                jason_file = json.load(file)
            
            new_data = {random_number:{"email":usr_email,"category":meal,"phone":phone_number,"date":today,"status":'',"foodname":food_item,"foodquantity":quantity,"foodprice":unit_price,"totalprice":unit_price*quantity,"OTP":""}}
            jason_file.update(new_data)
            with open("food_request.json","w") as file:
                json.dump(jason_file,file)


        if meal != '':
            return redirect(url_for('index'))
    else:

        return render_template('get_food_request.html')
    

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/loginindex')
def loginindex():
    return render_template('loginindex.html')
@app.route('/food_availability')
def food_availability():
    with open("food_availability.json","r") as file:
        jason_file = json.load(file)
    return render_template('food_availability.html',jason_file= jason_file)
@app.route('/food_request')
def food_request():
    with open("food_request.json","r") as file:
        jason_file = json.load(file)
    return render_template('food_request.html',jason_file= jason_file)

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/payment/<id>',methods=['GET','POST'])
def payment(id):
    global temp_id
    # id = request.form["id"]
    print(id)
    temp_id = id
   

    return render_template('payment.html')
@ app.route('/process_payment',methods=['GET','POST'])
def process_payment():
    food = ""
    sender_email = ""
    with open("food_availability.json","r") as file:
        jason_file = json.load(file)
        for i in jason_file:
            if i == temp_id:
                food = jason_file[i]['foodname']
                jason_file[i]['status'] = "paid"
                sender_email = jason_file[i]['email']
                with open("food_availability.json","w") as file:
                    json.dump(jason_file,file)
    with open("buying_orders.json","r") as file:
        jason_file = json.load(file)
        print(temp_id)
        otp = genarateOTP()
        jason_file[temp_id] = {"buyer_email":usr_email,"sender_email":sender_email,"date":today,"name":usr_name,"tp":usr_tp,"OTP":otp}
        # new_data = {usr_email:{"id":temp_id,"date":today,"name":usr_name,"tp":usr_tp,"OTP":otp}}
        # jason_file.update(new_data)
        with open("buying_orders.json","w") as file:
            json.dump(jason_file,file)
    return redirect(url_for('profile'))
        # for i in jason_file:
        #     if i == usr_email:
        #         print("sdfsdf")
        #         jason_file[i]['OTP'] = genarateOTP()
        #         with open("buying_orders.json","w") as file:
        #             json.dump(jason_file,file)
        #         return redirect(url_for('profile'))
    return render_template('index.html')
@app.route('/update_table/<id>',methods=['GET','POST'])
def update_table(id):
    with open("food_request.json","r") as file:
        jason_file = json.load(file)
    if id in jason_file:
        jason_file[id]['status'] = "proceeded"
        with open("food_request.json","w") as file:
            json.dump(jason_file,file)
        if jason_file[id]["email"] == usr_email:
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('food_request'))



@app.route('/proceed_requested_food',methods=['GET','POST'])
def proceed_requested_food():
    with open("food_availability.json","r") as file:
        jason_file = json.load(file)
    for i in jason_file:
        if jason_file[i]['email'] == usr_email:
            jason_file[i]['status'] = "proceed"
            with open("food_ava.json","w") as file:
                json.dump(jason_file,file)
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)

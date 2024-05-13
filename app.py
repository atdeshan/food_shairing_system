from flask import Flask, render_template,request,redirect, url_for, session
import secrets
import json

usr_email  = ""
usr_name = ""
usr_tp = ""
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# use_details = {"abc@gmail.com":"abc",'user2': 'password2', 'user3': 'password3'}

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
                print("pakaya")
                session['username'] = username
                
                if jason_file.get(i)["password"]==password:
                    global usr_email
                    global usr_name
                    global usr_tp
                    usr_email = i
                    usr_name = jason_file.get(i)["name"]
                    usr_tp = jason_file.get(i)["tp"]


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
    with open("food_availability.json","r") as file:
        jason_file = json.load(file)
        filtered_data = {email: user_data for email, user_data in jason_file.items() if email == usr_email}
    return render_template('profile.html',user_email = usr_email,user_name = usr_name,tp = usr_tp,json_file = filtered_data )
@app.route('/foodshare',methods=['GET','POST'])
def foodshare():
    if request.method == 'POST':
        meal = request.form['meals']
        food_item = request.form["foodname"]
        veg_non_veg = request.form["meal"]
        quantity = request.form["quantity"]
        phone_number = request.form["phoneno"]
        print(meal,food_item,veg_non_veg,quantity,phone_number)

        if meal != '':
            return redirect(url_for('index'))
    else:
        print("sdfsdf")
    return render_template('foodshare.html')
    

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/loginindex')
def loginindex():
    return render_template('loginindex.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(debug=True)

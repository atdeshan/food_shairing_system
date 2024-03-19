from flask import Flask, render_template,request,redirect, url_for, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
use_details = {"abc@gmail.com":"abc",'user2': 'password2', 'user3': 'password3'}

@app.route("/signin",methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        # Retrieve username and password from the form submission
        username = request.form['email']
        password = request.form['password']
        

        # Check if the submitted username exists and the password matches
        if username in use_details and use_details[username] == password:
            # Store username in session to indicate user is logged in
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # If username or password is incorrect, show an error message
            return "Invalid username or password. Please try again."
    return render_template('signin.html')
@app.route('/')
def index():
    # Check if user is logged in (i.e., session contains username)
    if 'username' in session:
        return render_template('index.html')
    else:
    
        return redirect(url_for('signin'))
    

@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/foodshare')
def foodshare():
    return render_template('foodshare.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, flash, session
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key="louisianapurchasecard"
# invoke the connectToMySQL function and pass it the name of the database we're usingcopy
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('mydb')
# now, we may invoke the query_db method
# print("all the users", mysql.query_db("SELECT * FROM users;"))

@app.route('/')
def index():
    all_registrations = mysql.query_db("SELECT * FROM registrations")
    print("All registered users", all_registrations, "\n")
    return render_template('index.html', registrations = all_registrations)

@app.route('/process', methods=['POST'])
def create():
    # Build our MySQL query here
    all_registrations = mysql.query_db("SELECT * FROM registrations")
    query = "INSERT INTO registrations (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
    data =  {
            'first_name': request.form['input_first_name'],
            'last_name':  request.form['input_last_name'],
            'email': request.form['input_email'],
            'password': request.form['input_password'],
            'password_confirm': request.form['input_confirm_password']
            }
    # Begin field validation
    if len(data['first_name']) < 2 :
        flash("First name must be 2 or more characters")
    if len(data['first_name']) < 2 :
        flash("Last name must be 2 or more characters")
    if len(data['password']) < 8 :
        flash("Password must be 8 or more characters")
    elif data['password'] != data['password_confirm'] :
        flash("Passwords must match!")
    if len(data['email']) < 2 :
        flash("Email required")
    for email in all_registrations:
        if data['email'] == email['email']:
            flash('Email is already taken!')
    # return "reserve"
    if '_flashes' in session.keys():
        return redirect("/")
    else:
        mysql.query_db(query, data)
        session["name"] = request.form['input_first_name']
        flash("You've been successfully registered")
        return render_template('/success.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    all_registrations = mysql.query_db("SELECT * FROM registrations")
    data =  {
            'email': request.form['login_email'],
            'password': request.form['login_password']
            }
    for email in all_registrations:
        if data['email'] == email['email'] and data['password'] == email['password']:
            session['logged_in']=True
            session["name"] = email['first_name']
            return render_template('/success.html')
        else:
            flash("That combo doesn't work!")
            redirect('/')

# How we will be logging out
@app.route('/destroy_session')
def destroy():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
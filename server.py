from flask import Flask, render_template, request, redirect
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
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
    query = "INSERT INTO registrations (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
    data =  {
            'first_name': request.form['input_first_name'],
            'last_name':  request.form['input_last_name'],
            'email': request.form['input_email'],
            'password': request.form['input_password'],
            'password_confirm': request.form['input_confirm_password']
            }
    mysql.query_db(query, data)
    return render_template('/success.html')

# How we might log out, also good for testing
@app.route('/destroy_session')
def destroy():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
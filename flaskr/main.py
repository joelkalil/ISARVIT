# Commands in PorwerShell (Windows)
# venv\Script\activate
# $env:FLASK_APP = "main"
# flask run

#---------------------------------------------- Imports ----------------------------------------------#
from flask import Flask, redirect, url_for, request, jsonify
from flask.templating import render_template
from flask_mysqldb import MySQL

#-----------------------------------------------------------------------------------------------------#
#----------------------------------------------- Flask -----------------------------------------------#

# Start Flask
app = Flask(__name__)

# Path of MySQL Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb'
mysql = MySQL(app)

#
# Observation: All API app route have in minimum one output in json format, in case this will be necessary. 
# The other possibilities render some html page.
#

# App route to start the principal layout
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# App to put the register in database
@app.route('/API/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        firstName = removeChars(request.form['firstName'])
        lastName = removeChars(request.form['lastName'])
        username = removeChars(request.form['username'])
        email = removeChars(request.form['email'])
        password = removeChars(request.form['password'])
    else:
        firstName = removeChars(request.args.get('firstName'))
        lastName = removeChars(request.args.get('lastName'))
        username = removeChars(request.args.get('username'))
        email = removeChars(request.args.get('email'))
        password = removeChars(request.args.get('password'))

    # Cursor.execute will return the count of the numbers of rows affected during the query
    # How Username is Primary Key, flag will be 0 (not exist) or 1 (exist)
    cursor = mysql.connection.cursor()

    try:
        # Check if have someone with this username
        flag = cursor.execute("SELECT * FROM users WHERE `Username` = %s", (username,))
        mysql.connection.commit()

        if flag:
            '''
            json = {
                "status" : "Failed",
                "message" : "Username already in use..."
            }
            return jsonify(json)
            '''
            print("Username already in use....")
            return index()
    except:
        #return jsonify(problemsCursor())
        print("Problems in cursor execution...")
        return index()

    try:
        cursor.execute("INSERT INTO users (FirstName, LastName, Username, Email, Password)  VALUES (%s, %s, %s, %s, %s)", (firstName, lastName, username, email, password))
        mysql.connection.commit()
        cursor.close()
        '''
        json = {
            "status" : "Succeed",
            "message" : "User created with success..."
        }
        return jsonify(json)
        '''
        print("User crated with success....")
        return redirect(url_for('user', name = firstName))
    except:
        #return jsonify(problemsCursor())  
        print("Problems in cursor execution...")
        return index()
    

# App to check if the couple username and password exist in database
@app.route('/API/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = removeChars(request.form['Login'])
        password = removeChars(request.form['password'])
    else:
        user = removeChars(request.args.get('Login'))
        password = removeChars(request.args.get('password'))

    cursor = mysql.connection.cursor()
    try:
        flag = cursor.execute("SELECT * FROM users WHERE `Username` = %s AND `Password` = %s", (user, password))
        data = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()

        if(flag):
            if (data[5]):
                # Case that the user is Admin
                '''
                json = {
                    "status" : "Succeed",
                    "message" : "Admin"
                }
                return jsonify(json)
                '''
                return redirect(url_for('admin', name = user))
            else:
                '''
                json = {
                    "status" : "Succeed",
                    "message" : "User"
                }
                return jsonify(json)
                '''
                return redirect(url_for('user', name = user))
        else:
            '''
            json = {
                "status" : "Failed",
                "message" : "Username or password incorrect!"
            }
            return jsonify(json)
            '''
            print("Username or password incorrect!")
            return index()
    except:
        #return jsonify(problemsCursor())  
        print("Problems in cursor execution...")
        return index()


# App to get all forms in database with the author is the user passed in URL
@app.route('/API/getForms/<User>', methods=['POST', 'GET'])
def allForms(User=None):
    cursor = mysql.connection.cursor()

    try:
        cursor.execute("SELECT * FROM forms WHERE `Creator` = %s", (User,))
        data = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        json = '['

        for row in range(len(data)):
            aux = {
                "FormName" : str(data[row][0]),
                "Creator" : str(data[row][1]),
                "Content" : str(data[row][2]),
                "FormID" : str(data[row][3]) 
            }

            json += str(aux)

            if not (row == len(data) - 1):
                json += ','
        json += ']'
        return jsonify(json)
    except:
        #return jsonify(problemsCursor())  
        print("Problems in cursor execution...")
        return index()

# App to add a new form in the database
@app.route('/API/addForm', methods=['POST', 'GET'])
def addForm():
    if request.method == 'POST':
        formName = request.form['formName']
        creator = request.form['creator']
        content = request.form['content']
    else:
        formName = request.args.get('formName')
        creator = request.args.get('creator')
        content = request.args.get('content')

    print(formName, creator, content)

    cursor = mysql.connection.cursor()

    try:
        cursor.execute("INSERT INTO forms (FormName, Creator, Content)  VALUES (%s, %s, %s)", (formName, creator, content))
        mysql.connection.commit()
        cursor.close()
        
        json = {
            "status" : "Succeed",
            "message" : ""
        }
        return jsonify(json)
        
        #return render_template('initial.html')
    except:
        return jsonify(problemsCursor())  
        print("Problems in cursor execution...")
        #return index()

# Apps to test login :
@app.route('/user/<name>')
def user(name):
    return 'welcome %s' % name

@app.route('/<name>')
def admin(name):
    return render_template('initial.html', name=name)

# Looping Flask
if __name__ == '__main__':
    app.run(debug=True)

#-----------------------------------------------------------------------------------------------------#
#------------------------------------------ Python Scripts -------------------------------------------#

# Function to remove some characters of data which will be put in MySQL by command, 
def removeChars(word):
    char = {'"', "'", '`'}
    for i in word:
        for c in char:
            if i == c:
                word = word.replace(i, '')
    return word


# This is a function that is called many times in this code, it returns a json in case of the cursor not works, if not we'll never
# know if we had some problem with him or not.
def problemsCursor():
    json = {
        "status" : "Failed",
        "message" : "Problems in cursor execution..."
    }
    return json
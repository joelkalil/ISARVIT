# Commands in PorwerShell (Windows)
# venv\Script\activate
# $env:FLASK_APP = "main"
# flask run

#---------------------------------------------- Imports ----------------------------------------------#
from flask import Flask, redirect, url_for, request, jsonify
from flask.templating import render_template
from flask_mysqldb import MySQL
import random

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

# Render Layouts
#
# App route to start the principal layout
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/templates/index.html', methods=['GET', 'POST'])
def index2():
    return render_template('index.html')

@app.route('/templates/documentation.html', methods=['GET', 'POST'])
def documentation():
    return render_template('documentation.html')

@app.route('/templates/about.html', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/templates/app.html', methods=['GET', 'POST'])
def application():
    return render_template('app.html')


#
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
            json = {
                "status" : "Failed",
                "error" : "Username already in use..."
            }
            return jsonify(json)
    except:
        return jsonify(problemsCursor())

    try:
        cursor.execute("INSERT INTO users (FirstName, LastName, Username, Email, Password)  VALUES (%s, %s, %s, %s, %s)", (firstName, lastName, username, email, password))
        mysql.connection.commit()

        hash = generateHash()

        if includeHash(username, hash, cursor):
            json = {
                "status" : "Succeed",
                "hash" : hash,
                "message" : "User created with success..."
            }
        else:
            json = {
                "status" : "Succeed",
                "error" : "Error in creation of hash",
                "message" : "User created with success..."
            }

        return jsonify(json)
    except:
        return jsonify(problemsCursor())
    

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

        if(flag):
            hash = generateHash()
            if changeHash(user, hash, cursor):
                if (data[5]):
                    # Case that the user is Admin
                    json = {
                        "status" : "Succeed",
                        "hash" : hash,
                        "class" : "Admin"
                    }
                    return jsonify(json)
                else:
                    json = {
                        "status" : "Succeed",
                        "hash" : hash,
                        "class" : "User"
                    }
                    return jsonify(json)
            else:
                json = {
                    "status" : "Succeed",
                    "error" : "Error in creation of hash",
                    "message" : "Username and password correct."
                }
        else:
            json = {
                "status" : "Failed",
                "error" : "Username or password incorrect!"
            }
            return jsonify(json)
    except:
        return jsonify(problemsCursor())  


# App to get all forms in database with the author is the user passed in URL
@app.route('/API/getForms/<user>/<hash>', methods=['POST', 'GET'])
def allForms(user=None, hash=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM forms WHERE `Creator` = %s", (user,))
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
            return jsonify(problemsCursor())  
    elif flag == "error":
        json = {
            "status" : "Failed",
            "error" : "Error in hash verification."
        }
        return jsonify(json)
    else:
        json = {
            "status" : "Failed",
            "error" : "Invalid hash."
        }
        return jsonify(json)

# App to add a new form in the database
@app.route('/API/addForm/<user>/<hash>', methods=['POST', 'GET'])
def addForm(user=None, hash=None):
    if request.method == 'POST':
        formName = request.form['formName']
        content = request.form['content']
    else:
        formName = request.args.get('formName')
        content = request.args.get('content')

    print(formName, user, content)

    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("INSERT INTO forms (FormName, Creator, Content)  VALUES (%s, %s, %s)", (formName, user, content))
            mysql.connection.commit()
            cursor.close()
            
            json = {
                "status" : "Succeed",
                "message" : ""
            }
            return jsonify(json)
            
        except:
            return jsonify(problemsCursor())
            
    elif flag == "error":
        json = {
            "status" : "Failed",
            "error" : "Error in hash verification."
        }
        return jsonify(json)
    else:
        json = {
            "status" : "Failed",
            "error" : "Invalid hash."
        }
        return jsonify(json)

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
        "error" : "Problems in cursor execution..."
    }
    return json

def generateHash():
    hash = random.getrandbits(128)
    hash = '%032x' % hash
    return hash

def includeHash(user, hash, cursor):
    try:
        cursor.execute("INSERT INTO `hash` (user, hash) VALUES (%s, %s)", (user, hash))
        mysql.connection.commit()
        cursor.close()
        return True
    except:
        return False

def changeHash(user, hash, cursor):
    try:
        cursor.execute("UPDATE `hash` SET `hash` = %s WHERE `user`= %s", (hash, user))
        mysql.connection.commit()
        cursor.close()
        return True
    except:
        return False

def checkHash(user, hash, cursor):
    try:
        # Check if have someone with this hash
        flag = cursor.execute("SELECT * FROM `hash` WHERE `user` = %s AND `hash` = %s", (user,hash))
        mysql.connection.commit()

        if flag:
            return True
        else: 
            return False
    except:
        return "error"
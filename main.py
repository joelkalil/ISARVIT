# Commands in PorwerShell (Windows)
# venv\Script\activate
# $env:FLASK_APP = "main"
# flask run

#---------------------------------------------- Imports ----------------------------------------------#
from distutils.log import error
from flask import Flask, redirect, url_for, request, jsonify
from flask.templating import render_template
from flask_mysqldb import MySQL
from datetime import date
import random

#-----------------------------------------------------------------------------------------------------#
#----------------------------------------------- Flask -----------------------------------------------#

# Start Flask
app = Flask(__name__)

'''
# Path of MySQL Database (localhost)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb_v2'
mysql = MySQL(app)
'''

# Path of MySQL Database (heroku)
app.config['MYSQL_HOST'] = 'eu-cdbr-west-02.cleardb.net'
app.config['MYSQL_USER'] = 'b58f94e8b79e2e'
app.config['MYSQL_PASSWORD'] = '9d765d57'
app.config['MYSQL_DB'] = 'heroku_038deda660564dd'
mysql = MySQL(app)

#
# Observation: All API app route have in minimum one output in json format, in case this will be necessary. 
#

# Render Layouts of Documentation
#
# App route to start the principal layout
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/templates/index.html', methods=['GET', 'POST'])
def index2():
    return render_template('index.html')

# Documentation layout
@app.route('/templates/documentation.html', methods=['GET', 'POST'])
def documentation():
    return render_template('documentation.html')

# About layout (removed from menu but still in code)
@app.route('/templates/about.html', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# App to show examples of requests
@app.route('/templates/app.html', methods=['GET', 'POST'])
def application():
    return render_template('app.html')

# Secret URL just tu be used to test something from backend
@app.route('/templates/testes.html', methods=['GET', 'POST'])
def testes():
    return render_template('testes.html')


# API Functions
#
# -------------------------------------------------------------------------------------------------------------------------- #
# App to put the register in database - OK!
@app.route('/API/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
    else:
        firstName = request.args.get('firstName')
        lastName = request.args.get('lastName')
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')

    # Cursor.execute will return the count of the numbers of rows affected during the query
    # How Username is Primary Key, flag will be 0 (not exist) or 1 (exist)
    cursor = mysql.connection.cursor()

    try:
        # Check if have someone with this username
        flag = cursor.execute("SELECT * FROM users WHERE `username` = %s", (username,))
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
        cursor.execute("INSERT INTO users (firstName, lastName, username, email, password, joined, favorites, recents, created)  VALUES (%s, %s, %s, %s, %s)", (firstName, lastName, username, email, password, date.today().year, '[]', '[]', '[]'))
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
    
# -------------------------------------------------------------------------------------------------------------------------- #
# App to check if the couple username and password exist in database - OK!
@app.route('/API/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['Login']
        password = request.form['password']
    else:
        user = request.args.get('Login')
        password = request.args.get('password')

    cursor = mysql.connection.cursor()
    try:
        flag = cursor.execute("SELECT * FROM users WHERE `username` = %s AND `password` = %s", (user, password))
        data = cursor.fetchone()
        mysql.connection.commit()

        if(flag):
            hash = generateHash()
            if changeHash(user, hash, cursor):
                if (data[10]):
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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to get all data from a user - OK!
@app.route('/API/getUserData/<user>/<hash>', methods=['POST', 'GET'])
def getUserData(user=None, hash=None):  
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM users WHERE `username` = %s", (user,))
            data = cursor.fetchone()
            mysql.connection.commit()
            cursor.close()

            json = '['

            aux = {
                "id" : str(data[0]),
                "username" : str(data[1]),
                "password" : str(data[2]),
                "firstName" : str(data[3]),
                "lastName" : str(data[4]),
                "email" : str(data[5]),
                "description" : str(data[6]),
                "joined" : str(data[7]), 
                "avatar" : str(data[8]), 
                "chips" : str(data[9]), 
                "admin" : str(data[10])
            }

            json += str(aux)

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to get rows data - OK!
#   Observation : I don't know if i'll return by creator or all rows, so for now i'll return all (check if Andreis)
@app.route('/API/getRows/<user>/<hash>', methods=['POST', 'GET'])
def getRows(user=None, hash=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM rows WHERE 1")
            data = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            json = '['

            for row in range(len(data)):
                aux = {
                    "editable" : str(data[row][0]),
                    "id" : str(data[row][1]),
                    "name" : str(data[row][2]),
                    "last_update" : str(data[row][3]),
                    "field" : str(data[row][4]),
                    "creator" : str(data[row][5]),
                    "preview" : str(data[row][6]),
                    "creator_avatar" : str(data[row][7]), 
                    "dynamic_image" : str(data[row][8]), 
                    "creator_id" : str(data[row][9]), 
                    "keywords" : str(data[row][10]),
                    "questions" : str(data[row][11]),
                    "uses" : str(data[row][12]),
                    "description" : str(data[row][13])
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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to get columns data - OK!
@app.route('/API/getColumns/<user>/<hash>', methods=['POST', 'GET'])
def getColumns(user=None, hash=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM columns WHERE 1")
            data = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()

            json = '['

            for row in range(len(data)):
                aux = {
                    "id" : str(data[row][0]),
                    "label" : str(data[row][1]),
                    "default" : str(data[row][2]),
                    "minWidth" : str(data[row][3]),
                    "align" : str(data[row][4])
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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to get all forms in database with the author is the user passed in URL - OK!
@app.route('/API/getForms/<user>/<hash>', methods=['POST', 'GET'])
def getForms(user=None, hash=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM forms WHERE `creator` = %s", (user,))
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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to get all forms in database with the author is the user passed in URL - OK!
@app.route('/API/getAllForms/<user>/<hash>', methods=['POST', 'GET'])
def getAllForms(user=None, hash=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT * FROM forms WHERE 1")
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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to add a new form in the database - OK!
@app.route('/API/addForm/<user>/<hash>', methods=['POST', 'GET'])
def addForm(user=None, hash=None):
    if request.method == 'POST':
        formName = request.form['formName']
        content = request.form['content']
        template = request.form['template']
        imageName = request.form['imageName']
        begin = request.form['begin']
        end = request.form['end']
        image = request.form['image']
    else:
        formName = request.args.get('formName')
        content = request.args.get('content')
        template = request.args.get('template')
        imageName = request.args.get('imageName')
        begin = request.args.get('begin')
        end = request.args.get('end')
        image = request.args.get('image')

    print(formName, user, content)

    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("INSERT INTO forms (formName, creator, content)  VALUES (%s, %s, %s)", (formName, user, content))
            mysql.connection.commit()

            cursor.execute("SELECT FormID FROM `forms` WHERE formName = %s", (formName,))
            data = cursor.fetchone()
            mysql.connection.commit()
            formID = data[0]

            cursor.execute("INSERT INTO templates (template, formID) VALUES (%s, %s)", (template, formID))
            mysql.connection.commit()

            cursor.execute("INSERT INTO images (imageName, begin, end, image, formID) VALUES (%s, %s)", (imageName, begin, end, image, formID))
            mysql.connection.commit()

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to change user's information (since a data until all) - OK!
@app.route('/API/changeUserInfo/<user>/<hash>', methods=['POST', 'GET'])
def changeUserInfo(user=None, hash=None):
    if request.method == 'POST':
        dataToChange = stringToList2(request.form['dataToChange'])
        content = stringToList2(request.form['content'])

    else:
        dataToChange = stringToList2(request.args.get('dataToChange'))
        content = stringToList2(request.args.get('content'))

    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            size = len(dataToChange)

            query = 'UPDATE users SET '
            for i in range(size):
                if i < size - 1:
                    query += str(dataToChange[i]) + ' = %s, '
                else:
                    query += str(dataToChange[i]) + ' = %s WHERE username = %s'

            content.append(user)
            dataContent = tuple(content)

            cursor.execute(query, dataContent)
            mysql.connection.commit()

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to set a formulary to favorite - OK!
@app.route('/API/setFavorite/<user>/<hash>/<formName>', methods=['POST', 'GET'])
def setFavorite(user=None, hash=None, formName=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT FormID FROM `forms` WHERE formName = %s", (formName,))
            data = cursor.fetchone()
            mysql.connection.commit()
            formID = data[0]

            cursor.execute("SELECT favorites FROM `users` WHERE username = %s", (user,))
            data = cursor.fetchone()
            mysql.connection.commit()

            favorites = stringToList(data[0])
            flag_favorite = False

            for i in range(len(favorites)):
                if favorites[i] == formID:
                    flag_favorite = True

            if flag_favorite:
                json = {
                    "status" : "Succeed",
                    "message" : "Formulary was already a favorite."
                }
                return jsonify(json)
            else:
                favorites.append(formID)
                favorites = str(favorites)
                cursor.execute("UPDATE users SET favorites = %s WHERE username = %s", (favorites, user))
                mysql.connection.commit()

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to remove a formulary from favorites - OK!
@app.route('/API/removeFavorite/<user>/<hash>/<formName>', methods=['POST', 'GET'])
def removeFavorite(user=None, hash=None, formName=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT FormID FROM `forms` WHERE formName = %s", (formName,))
            data = cursor.fetchone()
            mysql.connection.commit()
            formID = data[0]

            cursor.execute("SELECT favorites FROM `users` WHERE username = %s", (user,))
            data = cursor.fetchone()
            mysql.connection.commit()
            favorites = stringToList(data[0])

            for i in range(len(favorites)):
                if favorites[i] == formID:
                    favorites.pop(i)
                    break

            favorites = str(favorites)

            cursor.execute("UPDATE users SET favorites = %s WHERE username = %s", (favorites, user))
            mysql.connection.commit()

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to add a formulary in created - OK!
@app.route('/API/addCreated/<user>/<hash>/<formName>', methods=['POST', 'GET'])
def addCreated(user=None, hash=None, formName=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT FormID FROM `forms` WHERE formName = %s", (formName,))
            data = cursor.fetchone()
            mysql.connection.commit()
            formID = data[0]

            cursor.execute("SELECT created FROM `users` WHERE username = %s", (user,))
            data = cursor.fetchone()
            mysql.connection.commit()
            created = stringToList(data[0])

            flag_created = False

            for i in range(len(created)):
                if created[i] == formID:
                    flag_created = True

            if flag_created:
                json = {
                    "status" : "Succeed",
                    "message" : "Formulary was already associated to this user."
                }
                return jsonify(json)
            else:
                created.append(formID)
                created = str(created)
                cursor.execute("UPDATE users SET created = %s WHERE username = %s", (created, user))
                mysql.connection.commit()

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

# -------------------------------------------------------------------------------------------------------------------------- #
# App to remove a formulary from created - OK!
@app.route('/API/removeCreated/<user>/<hash>/<formName>', methods=['POST', 'GET'])
def removeCreated(user=None, hash=None, formName=None):
    cursor = mysql.connection.cursor()

    flag = checkHash(user, hash, cursor)

    if flag:
        try:
            cursor.execute("SELECT FormID FROM `forms` WHERE formName = %s", (formName,))
            data = cursor.fetchone()
            mysql.connection.commit()
            formID = data[0]

            cursor.execute("SELECT created FROM `users` WHERE username = %s", (user,))
            data = cursor.fetchone()
            mysql.connection.commit()
            created = stringToList(data[0])

            for i in range(len(created)):
                if created[i] == formID:
                    created.pop(i)
                    break
            
            created = str(created)
            cursor.execute("UPDATE users SET created = %s WHERE username = %s", (created, user))
            mysql.connection.commit()

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

# This is a function that is called many times in this code, it returns a json in case of the cursor not works, if not we'll never
# know if we had some problem with him or not.
#
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

def stringToList(array):
    lista = []

    array = array.replace("'", '')
    
    last = len(array)
    
    new_array = str(array[1:last-1])
    
    lista = new_array.split(',')

    if lista[0] == '':
        lista = []
    else:
        lista = [int(i) for i in lista]
    
    return lista

def stringToList2(array):
    lista = []

    array = array.replace("'", '')
    
    last = len(array)
    
    new_array = str(array[1:last-1])
    
    lista = new_array.split(',')

    if lista[0] == '':
        lista = []
    
    return lista
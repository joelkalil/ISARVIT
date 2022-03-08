# ISARVIT

ISARVIT is a very nice web application based around the simple idea of making the generation of Medical Reports Easier. It started as a student project under Mr. Slim Hammadi (researcher at CRIStAL and professor at Centrale Lille) and the Centre Hospitalier Universitaire de Lille.

This was a project which I participated with more 11 students during 2 years in Centrale Lille, I was the head of the back-end and the responsible to develop an API in python using flask.

# 1. Backend
![](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)

The backend is developed in Python, using the framework Flask (with some libraries) and hosted in Heroku. The idea was done an API to help the frontend to change information with a database hosted using MySQL, this should include cryptographic and make a safe environment. You can see the live version [here](https://api-isarvit.herokuapp.com).

To run the backend in your machine, you need to have [FLASK](https://flask.palletsprojects.com/en/2.0.x/) installed. The tutorial to install from zero in your machine are :

If you already have Python3 intalled, skip to step 2.

**Step 1: Install Python3**

Windows:
```bash
pip install python3
```
Linux:
```bash
sudo apt install python3
```
**Step 2: Prepare the environment**

So create a separate directory for your project and execute :
```bash
mkdir <project name>
```
After, open this directory :
```bash
cd <project name>
```
And then create a virtual env :
```bash
python3 -m venv <name of environment>
```
**Step 3: Activate the environment**

Windows:
```bash
<name of environment>\Scripts\activate
```
Linux:
```bash
.<name of environment>/bin/activate
```
**Step 4: Install FLask in environment**

```bash
pip install Flask
```
**Step 5: Install requirements**

```bash
pip install -r requirements.txt
```
**Step 6: Configure Flask**

In venv set the main.py to be executed in Flask with the command:

Windows:
```bash
$env:FLASK_APP:"<name of file>.py"
```
Linux:
```bash
export FLASK_APP=<name of file>.py
```
After that, use this command to run the application:
```bash
flask run
```

*Observation: If you want use a local database [Mysql](https://www.mysql.com), you can find a script in **API/static/MySQL/make** to create the database necessary for the application.*

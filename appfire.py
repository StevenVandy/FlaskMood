from flask import Flask, render_template, url_for, request, redirect, session
from datetime import datetime
import pyrebase

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyCEm1Ldgo_KrhwHthn2c5eC1A79ysKsSKs",
  "authDomain": "pyrebasetest-1c50a.firebaseapp.com",
  "databaseURL": "https://pyrebasetest-1c50a.firebaseio.com",
  "projectId": "pyrebasetest-1c50a",
  "storageBucket": "pyrebasetest-1c50a.appspot.com",
  "messagingSenderId": "223737136097",
  "appId": "1:223737136097:web:bf5906b85f236852"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

auth = firebase.auth()
# user=auth.sign_in_with_email_and_password(email,password)
# auth.get_account_info(user['idToken'])

#app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

class DataStore():
    user = None

data = DataStore()

@app.route('/', methods=['POST', 'GET'])
def index():
    if data.user == None:
        return redirect('login')       
    else:
        if request.method == 'POST':
            data_to_upload={
                'mood' : request.form['content'],
                'date' : datetime.now().strftime("%m/%d/%Y"),
                'time' : datetime.now().strftime("%H:%M:%S")
            }
            try:
                db.child("moods").push(data_to_upload,data.user['idToken'])
                return render_template('index.html', user=data.user)
            except:
                redirect('login')
        else:
            return render_template('index.html', user=data.user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        try:
            user=auth.sign_in_with_email_and_password(request.form['username'],request.form['password'])
            data.user=user
            return redirect('/')
        except:
            error = 'Invalid Credentials. Please try again.'
            render_template('login.html', error=error)
    return render_template('login.html', error=error)



if __name__ == "__main__":
    app.run(debug=True)

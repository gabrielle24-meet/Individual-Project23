from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase




app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
"apiKey": "AIzaSyAFSxExGBR4zkhGJRK_Xb-BFz3mE5T4nBM", 
  "authDomain": "example-9e0f4.firebaseapp.com",
  "projectId": "example-9e0f4",
  "storageBucket": "example-9e0f4.appspot.com",
  "messagingSenderId": "5891476454" ,
  "appId": "1:5891476454:web:920a5f8c52b0041e9be427",
 "measurementId": "G-LXM8YFZZ2B",
 "databaseURL": "https://example-9e0f4-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def create_acc():
    error = ""
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email": username, "password": password, "username" : username}
            db.child("Users").child(UID).set(user)
            return redirect(url_for("comments"))
        except:
            error = "Authentication failed"
            print("please try again")

    return render_template("create_acc.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
     error = ""
     if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('comments'))
        except:
            print("please try again")
     return render_template("signin.html")



@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
    




@app.route('/comments', methods = ['GET', 'POST'])
def comments():
    error = ""
    if request.method == "POST":
        try:   
            username = request.form["username"]
            comment = request.form["text"]
            comments2 = {"username": username, "comment": comment}
            db.child("comments").push(comments2)
            return redirect(url_for('all_comments'))
        except:
            error = "An error occurred while adding the comment."
    return render_template("comments.html", error=error)



@app.route('/all_comments', methods=['GET'])
def all_comments():
    comments_data = db.child("comments").get().val()
    username = login_session.get('user', {}).get('email', '')  
    return render_template("all_comments.html", comments=comments_data, username=username)









#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)
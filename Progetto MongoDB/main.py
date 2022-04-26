from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = connect.Progetto
collection = db.Dati



@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = collection.find_one({"name": user})
        email_found = collection.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'Nome': user, 'Email': email, 'Password': hashed,'NomeUtente': user}
            collection.insert_one(user_input)
            print("Ho inserito i collection")
            
            user_data = collection.find_one({"Email": email})
            new_email = user_data['Email']
   
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')
    
    
    
if __name__ == "__main__":
  app.run(debug=True)
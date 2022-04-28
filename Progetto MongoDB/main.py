from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('Progetto')
dati = db.Dati



@app.route("/", methods=['post', 'get'])
def registrazione():
    message = ''
    if "Email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = dati.find_one({"name": user})
        email_found = dati.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('registrazione.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('registrazione.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('registrazione.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'Nome': user, 'Email': email, 'Password': hashed,'NomeUtente': user}
            dati.insert_one(user_input)
            print("Ho inserito i dati")
            
            user_data = dati.find_one({"Email": email})
            new_email = user_data['Email']
   
            return render_template('logged_in.html', email=new_email)
    return render_template('registrazione.html')
    
    
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = dati.find_one({"Email": email})
        if email_found:
            email_val = email_found['Email']
            passwordcheck = email_found['Password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)
    
@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        
        return render_template('logged_in.html', email=email)
    else:
        return redirect(url_for("login"))    


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("login.html")
    else:
        return render_template('registrazione.html')
        
        
        
        
        
@app.route("/creapartita", methods=["POST", "GET"])
def ListaPartita():
    
    
    



    return render_template('listagame.html',**vars())
        
if __name__ == "__main__":
  app.run(debug=True)
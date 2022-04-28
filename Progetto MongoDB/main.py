from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import random

app = Flask(__name__)
app.secret_key = "testing"

client = pymongo.MongoClient("localhost:27017")

#get the database name
db = client.get_database('Progetto')
#get the particular collection that contains the data
collection = db.Dati
 



@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    x = random.randint(0,10000)
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
            
            post={"_id":x,"Nome":user,"email":email,"password":hashed,"NomeUtente":user}
            collection.insert_one(post)
            user_data = collection.find_one({"Email": email})
            new_email = user_data['email']
   
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route("/inserisci")
def ciao():
    x = random.randint(0,10000)

    db.collection.insert_one({'_id':52,'Nome': "ciao", 'Email': "ciao", 'Password': "ciao",'NomeUtente': "ciao"})




    return ("Ciao ho inserito")
    
    
if __name__ == "__main__":
  app.run(debug=True)
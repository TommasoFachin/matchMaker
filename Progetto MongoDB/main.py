from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt
import string
import re
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
            message = 'Esiste già un utente con quel nome'
            return render_template('registrazione.html', message=message)
        if email_found:
            message = 'Questa email è gia esistente nel db'
            return render_template('registrazione.html', message=message)
        if password1 != password2:
            message = 'Le password non corrispondono!!'
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
    message = 'Fai qui il tuo login'
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
                message = 'Password sbagliata!'
                return render_template('login.html', message=message)
        else:
            message = 'Email non trovata'
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
        
        
        
        
        
@app.route("/listapartite", methods=["POST", "GET"])
def ListaPartite():
    if "email" in session:
        email = session["email"]
        data=db.get_collection("Partite")
        lista = []
    #filter = {'username': 1, 'user_posts': 1, '_id': 0}
    # partite = db.data.find_one({'email' : email, 'password' : password}, {'_id': 1})
        uno = data.find({},{'Sport': 1, 'Codice': 1, '_id': 0})         #stampare roba
    # for row in uno:
        # print(row)
        # lista.append(row)
        
        
    
        for row in uno:
            numero=str(row)
            numeromodificato = re.sub("[^0-9]", "",numero)
            lista.append(numeromodificato)
        print(email)
    else:
        return redirect(url_for("login"))
    #print(lista)
    
    
    
    
    
    # x = db.student.find({}, {"Sport":0, '_id':0,'Codice':0,'P1':0,'P2':0})

    # for each_doc in x:
        # print(each_doc)
    



    return render_template('listagame.html',**vars())
    
@app.route(("/partita"), methods=["POST", "GET"])    
def Partita():
    if "email" in session:
        email=session['email']
        
        
        
    
    
    
    
    else:
       return redirect(url_for("login"))
    


    return render_template('partita.html',**vars())
    
    
@app.route (("/creaPartita"), methods=["POST", "GET"])   
def creaPartita():
        
        
        
    return render_template('creaPartita.html',**vars())
        
@app.route (("/conferma"), methods=["POST", "GET"])
def inserisciPartita():
    data=db.get_collection("Partite")
    email = session['email']
    codice=request.form['codice']
    sport = request.form['sport']
    print (codice)
    print (sport)
    
    print(email)
    
    data.insert_one({'Sport':sport,'Codice':codice,'P1':email,'P2':''})
    
    
    
    
    


    return render_template('confirmed.html',**vars())

@app.route (("/IcrizioneConfermata"), methods=["POST", "GET"])
def inserisciGiocatore():



    return render_template('confirmed.html',**vars())
    
      
if __name__ == "__main__":
  app.run(debug=True)
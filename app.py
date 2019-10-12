from flask import Flask,render_template,make_response
from flask import request,session,redirect,url_for
import pymysql as sql
app = Flask(__name__)
app.secret_key = "fofohforfoff84947594bfhbfibfjnfjnfjn"
@app.route("/")
def home():
    return render_template("header.html")

@app.route("/<user>")
def index(user):
    return render_template("one.html",u=user)
    #return "Hello world"

@app.route("/home/")
def index1():
    dict = {
        'name' : 'simran',
        'course' : 'python',
        'year' : 2019,
    }
    return render_template("one.html",d=dict)

@app.route("/hello/")
def hello():
    return "<h1 style='color:red'>Welcome to my first flask project</h1>"

@app.route("/login/")
def login():
    if request.cookies.get('islogin'):
        error = 'Already logged in...'
        return render_template("data.html",error=error)
    else:
        return render_template("login.html")

@app.route("/login1/",methods=['GET','POST'])
def login1():
    if request.method == "POST":
        email = request.form.get('email')
        try:
            db = sql.connect(host="localhost",port=3306,user="root",password="",database="advancebatch")
            c = db.cursor()
            cmd = "select * from user where email='{}'".format(email)
            c.execute(cmd)
            data = c.fetchone()
            #print(data)
            password = request.form.get('pass')
            if data:
                if password == data[3]:
                    session['email'] = email
                    session['islogin'] = 'true'
                    return render_template("data.html")
                    #resp = make_response(render_template("data.html"))
                    #resp.set_cookie('email',email)
                    #resp.set_cookie('islogin','True')
                    #return resp
                    #return "<h1 style='color:red'>Welcome user {} with password {}".format(email,password)
                else:
                    error = "Password does not match....Try Again"
                    return render_template("login.html",error=error)
            else:
                error = "User does not exist....Signup to login"
                return render_template("signup.html",error=error)
        except Exception as e:
            return "Error.....{}".format(e)

@app.route('/signup/')
def signup():
    return render_template("signup.html")

@app.route('/signup1/',methods=['GET','POST'])
def signup1():
    if request.method == "POST":
        try:
            db = sql.connect(host="localhost",port=3306,user='root',password='',database="advancebatch")
            c = db.cursor()
            firstname = request.form.get('fname')
            lastname = request.form.get('lname')
            email = request.form.get('email')
            password = request.form.get('pass')
            cpassword = request.form.get('cpass')
            pic = request.form.get('myfile')
            f = request.files['myfile']
            #print(f)
            fn = f.filename
            fn = fn.split('.')[-1]
            f.save("static/images/"+email+'.'+fn)
            print(fn)
            if password == cpassword:
                cmd = "insert into user values('{}','{}','{}','{}','{}')".format(firstname,lastname,email,password,pic)
                c.execute(cmd)
                db.commit()
                return render_template("one.html")
            else:
                error = "Password does not match...Try again"
                return render_template("signup.html",error=error)
        except Exception as e:
            return "Error......{}".format(e)

@app.route('/logout/')
def logout():
    #resp = make_response(render_template("login.html"))
    #resp.delete_cookie('email')
    #resp.delete_cookie('islogin')
    #return resp
    del session['email']
    del session['islogin']
    return redirect(url_for('login'))
    #return render_template("login.html")
if __name__ == "__main__":
    app.run(host="localhost",port=80,debug=True)
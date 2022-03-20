from flask import Flask,render_template,request
app = Flask(__name__)

# For Database
from flask_mysqldb import MySQL

app= Flask(__name__)

#Database settings for  mysql
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db_trekapp'

mysql=MySQL(app) #initallizing mysql



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/doLogin',methods=['POST'])
def doLogin():
    #presentation layer ma submit vaako data application layer ma request garera lyako
    email=request.form['email']
    password=request.form['psw']

    #cursor is use  to hit the queries
    cursor = mysql.connection.cursor()
    resp=cursor.execute( '''SELECT * FROM users WHERE email=%s and password=%s;,''',(email,password))

    user=cursor.fetchone() #fetch() retuns the value in tupple forms
    print(cursor.fetchone()) #print alll the info of  1'st  user
    print(resp)
    print(type(resp))
    cursor.close()

    # if email == "roshan@gmail.com" and password == "12345":
        #  return render_template('home.html',result={"email":email})
    if resp == 1:
        return render_template('home.html',result=user)

    else:
        return render_template('login.html',result="Invalid credentials")

@app.route('/doRegister',methods=['post'])
def doRegister():
    full_name=request.form['full_name']
    email=request.form['email']
    phone_number=request.form['phone_number']
    address=request.form['address']
    password=request.form['psw'] 
    cursor=mysql.connection.cursor()
    cursor.execute('''INSERT INTO users VALUES(NULL,%s,%s,%s,%s)''',(full_name,email,phone_number,password))
    mysql.connection.commit() #to write the data into databse we must commit()//for insert(),update()
    cursor.close()

    return render_template('login.html',result="Registered Successfully,Please login to continue...")

    
if __name__ == '__main__':
    app.run()

from flask import Flask , render_template , request , redirect , url_for
from flask_mysqldb import MySQL


app = Flask(__name__)           # __name_ : flaskapp.py

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root123"
app.config["MYSQL_DB"]="pydb"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)



@app.route('/')
@app.route('/home')
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM pythontable"
    con.execute(sql)
    result = con.fetchall()
    return render_template('home.html',data = result)

@app.route("/newuser" , methods=['GET' , 'POST'])
def addusers():
    if request.method=='POST':
        id = request.form['empid']
        name = request.form['empname']
        sal = request.form['empsalary']
        con=mysql.connection.cursor()
        sql=f"INSERT INTO pythontable (employee_id,employee_name,salary) VALUES ({id},'{name}',{sal});"
        con.execute(sql)
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template('newuser.html')


@app.route("/deleteuser" , methods=['GET','POST'])
def deleteuser():
    if request.method=='POST':
        id=request.form['empid']
        con=mysql.connection.cursor()
        sql=f"DELETE FROM pythontable WHERE employee_id = {id};"
        con.execute(sql)
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template('delete.html')

@app.route("/edituser/<string:id>",methods=['GET','POST'])
def edituser(id):

    con=mysql.connection.cursor()
    if request.method == 'POST':
        eid = request.form['empid']
        name = request.form['empname']
        sal = request.form['empsalary']
        sql = f"UPDATE pythontable SET employee_id = {eid} , employee_name = '{name}' , salary = {sal} WHERE employee_id = {eid}"
        con.execute(sql)
        mysql.connection.commit()
        con.close()
        return  redirect(url_for("home"))
    con = mysql.connection.cursor()
    sql = "SELECT * FROM pythontable WHERE employee_id = %s"
    con.execute(sql,[id])
    res = con.fetchone()
    return  render_template('edituser.html',data=res)


if __name__ == '__main__':          #flaskapp.py == mainfile:
    app.run(debug=True)



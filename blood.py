from flask import Flask,render_template,request
import sqlite3 as sql

app=Flask(__name__)

#Homepage
@app.route('/')
def home():
    return render_template('home.html')



#Donor Registration
@app.route('/donor',methods=['GET','POST'])
def donor_resgister():
    if(request.method=='GET'):
        return render_template('donor_register.html')
    else:
        return render_template('home.html')

#Donor Submission
@app.route('/success_donor',methods=['GET','POST'])
def success_donor():
    if(request.method=='POST'):
        try:
            name=request.form['name']
            city=request.form['city']
            phone=request.form['phone']
            blood=request.form['blood']
            weight=request.form['weight']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT OR IGNORE INTO donor(name,city,bloodgroup,phone,weight)VALUES(?,?,?,?,?)",(name,city,blood,phone,weight))
                con.commit()
                msg="Record Successfully Added"
        except:
            con.rollback()
            msg="Error in Inserion"
        finally:
            return render_template('succes.html',msg=msg)
            con.close()

#Receiver Registration
@app.route('/receiver',methods=['GET','POST'])
def receiver_login():
    if(request.method=='GET'):
        return render_template('receiver_redirect.html')
    else:
        return render_template('home.html')

@app.route('/receiver_register',methods=['GET','POST'])
def receiver_register():
    if(request.method=='GET'):
        return render_template('receiver_register.html')
    else:
        return render_template('home.html')


#Receiver Submission
@app.route('/success_receiver',methods=['GET','POST'])
def success_receiver():
    if(request.method=='POST'):
        try:
            name=request.form['name']
            passwd=request.form['passw']
            city=request.form['city']
            phone=request.form['phone']
            blood=request.form['blood']
            with sql.connect("database.db") as con:
                cur=con.cursor()
                cur.execute("INSERT OR IGNORE INTO receiver(name,passwd,city,bloodgroup,phone)VALUES(?,?,?,?,?)",(name,passwd,city,blood,phone))
                con.commit()
                msg="Record Successfully Added"
        except:
            con.rollback()
            msg="Error in Inserion"
        finally:
            return render_template('succes.html',msg=msg)
            con.close()

#Login Receiver
@app.route('/login_receiver',methods=['GET','POST'])
def login_receiver():
    if(request.method=='POST'):
        name=request.form['id']
        passwd=request.form['passw']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from receiver")
        rows=cur.fetchall()
        nameDB=[]
        passDB=[]
        for r in rows:
            nameDB.append(str(r['name']))
            passDB.append(str(r['passwd']))
        if(nameDB[0]==name and passDB[0]==passwd):
            cur.execute("select * from donor")
            rows=cur.fetchall()
            return render_template('list_of_donor.html',rows=rows)
        else:
            msg="Invalid Login, Login Again"
            return render_template('failure.html',msg=msg)


#About BloodDonationCamp
@app.route('/about_blood',methods=['GET','POST'])
def about_blood():
    if(request.method=='GET'):
        return render_template('about.html')
    else:
        msg="Error"
        return render_template('failure.html',msg=msg)

#Admin Login
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if(request.method=='GET'):
        return render_template('admin.html')
    else:
        return render_template('home.html')

#Receiver Deletion
@app.route('/delrec/<sd>')
def delrec(sd):
	try:
		con = sql.connect('database.db')
		cursor = con.cursor()
		cursor.execute("DELETE FROM receiver WHERE phone = '%s' "% sd)
		con.commit()
		msg = "Receiver Deleted"
	except Error as error:
		print(error)

	finally:
		return render_template('success1.html',msg=msg)
		cursor.close()
		con.close()

#Donor Deletion
@app.route('/deldon/<name>')
def deldon(name):
	try:
		con = sql.connect('database.db')
		cursor = con.cursor()
		cursor.execute("DELETE FROM donor WHERE phone = '%s' "% name)
		con.commit()
		msg = "Donor Deleted"
	except Error as error:
		print(error)

	finally:
		return render_template('success1.html',msg=msg)
		cursor.close()
		con.close()

#Admin Detail
@app.route('/admin_detail',methods=['GET','POST'])
def admin_detail():
    if(request.method=='POST'):
        name=request.form['name']
        passwd=request.form['passw']
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM admin")
        rows=cur.fetchall()
        nameDB=str(rows[0]['id'])
        passDB=str(rows[0]['password'])
        if(nameDB==name):
            return render_template('details_admin.html')
        else:
            msg="Invalid Login"
            return render_template('failure.html',msg=msg)

#Donor Details
@app.route('/donor_details',methods=['GET','POST'])
def donor_details():
    if(request.method=='POST'):
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from donor")
        rows=cur.fetchall()
        return render_template('details_donor.html',rows=rows)
    else:
        return render_template('details_admin.html')

#Receiver Details
@app.route('/receiver_details',methods=['GET','POST'])
def receiver_details():
    if(request.method=='POST'):
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from receiver")
        rows=cur.fetchall()
        return render_template('details_receiver.html',rows=rows)
    else:
       	return render_template('details_admin.html')

#Search
@app.route('/Search',methods=['GET','POST'])
def Search():
    bgroup = request.form['search2']
    if(request.method=='POST'):
        con=sql.connect("database.db")
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("select * from donor where bloodgroup = '%s' "% bgroup)
        rows=cur.fetchall()
        return render_template('list_of_donor.html',rows=rows)
    else:
        msg = "Not Found"
        return render_template('failure.html',msg=msg)

if __name__ == '__main__':
    app.run(debug=True)

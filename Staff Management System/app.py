from flask import Flask,render_template,redirect,session,url_for,flash,request
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
import werkzeug.wrappers
import os
import base64
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'SMS PROJECT'

upload_image='static/'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root123'
app.config['MYSQL_DB'] = 'mysms'
app.config['MYSQLDB.CURSORS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = upload_image
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

  
mysql = MySQL(app)



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def sms_home():
    return render_template("sms_home.html")
#admin
@app.route('/Admin_home',methods=['GET','POST'])
def admin_home():
    if request.method == 'POST':
        adminid = request.form['adminid']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM admin WHERE adminid = %s AND password = %s', (adminid, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['adminid'] = account['adminid']
            success= 'Logged in Successfully....!'
            #s[adminid]=account[adminid]
            name=account[0]
            return render_template('admin_home.html',name=name,success=success)
        else:
            error = '  Incorrect admin / password....!'
            return render_template('sms_home.html',error=error)
        mysql.connection.commit()
        cursor.close()   
    return render_template('sms_home.html')
        
        

#user
@app.route('/user_home',methods=['GET','POST'])
def user_home():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE userid = %s AND password = %s' , (userid,password))
        data = cursor.fetchone()
        if data:
            session['loggedin'] = True
            userid=data[0]
            username=data[2]
            success= 'Logged in Successfully....!'
            return render_template('user_home.html',userid=userid,success=success)
        else:
            error = '  Incorrect username / password....!'
            return render_template('sms_home.html',error=error)
            mysql.connection.commit()
            cursor.close()
            
            
@app.route('/user_home1',methods=['GET','POST'])
def user_home1():
    if request.method == 'POST':
        staffid=request.form['staffid']
        success= 'Logged in Successfully....!'
        return render_template('user_home.html',userid=staffid,success=success)


#register
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method=='POST':
        userid = request.form['userid']
        password = request.form['password']
        username = request.form['username']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO register(userid,password,username) VALUES(%s,%s,%s)', (userid,password,username))
        mysql.connection.commit()
        cursor.close()
        success= 'Registration Completed Successfully....!'
        return render_template('sms_home.html',success=success)
        
        
#Forget Password

@app.route('/Forget_Password', methods =['GET', 'POST'])
def Forget_Password():
    if request.method=='POST':
        userid = request.form['userid']
        Npassword = request.form['Npassword']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE register SET password=%s WHERE userid=%s',(Npassword,userid))
        mysql.connection.commit()
        cursor.close()
        success='Password Reseted Successfully....! '
        return render_template('user_home.html',success=success,userid=userid) 

@app.route('/logout')
def logout():
    return redirect(url_for('sms_home'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/viewuser')
def viewuser():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM register')
    user = cursor.fetchall()
    return render_template('admin_home.html',userdata=user,name='admin')
    mysql.connection.commit()
    cursor.close()



#delete user
@app.route('/delete_user/<string:id>')
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM register WHERE userid=%s',[id])
    mysql.connection.commit()
    cursor.close() 
    return redirect(url_for('viewuser'))
    




#faculty_details

@app.route('/faculty_details',methods=['GET','POST'])
def faculty_details():
    if request.method=='POST':
        staffid=request.form['staffid']
        staffname=request.form['name']
        designation=request.form['designation']
        Department=request.form['Department']
        datefield=request.form['datefield']
        address=request.form['address']
        phone=request.form['phone']
        email=request.form['email']
        image=request.files['image']
        degree1=request.form['degree1']
        college1=request.form['college1']
        yearpassing1=request.form['yearpassing1']
        percentage1=request.form['percentage1']
        degree2=request.form['degree2']
        college2=request.form['college2']
        yearpassing2=request.form['yearpassing2']
        percentage2=request.form['percentage2']
        degree3=request.form['degree3']
        college3=request.form['college3']
        yearpassing3=request.form['yearpassing3']
        percentage3=request.form['percentage3']
        course1=request.form['course1']
        cfrom1=request.form['cfrom1']
        cto1=request.form['cto1']
        experience1=request.form['experience1']
        course2=request.form['course2']
        cfrom2=request.form['cfrom2']
        cto2=request.form['cto2']
        experience2=request.form['experience2']
        course3=request.form['course3']
        cfrom3=request.form['cfrom3']
        cto3=request.form['cto3']
        experience3=request.form['experience3']
        Areaofinterest=request.form['AreaofInterest']
        Achievement=request.form['Achievement']
        researchtitle1=request.form['researchtitle1']
        jc1=request.form['jc1']
        pdate1=request.form['pdate1']
        ni1=request.form['ni1']
        researchtitle2=request.form['researchtitle2']
        jc2=request.form['jc2']
        pdate2=request.form['pdate2']
        ni2=request.form['ni2']
        researchtitle3=request.form['researchtitle3']
        jc3=request.form['jc3']
        pdate3=request.form['pdate3']
        ni3=request.form['ni3']
        researchtitle4=request.form['researchtitle4']
        jc4=request.form['jc4']
        pdate4=request.form['pdate4']
        ni4=request.form['ni4']
        ptitle1=request.form['ptitle1']
        famount1=request.form['famount1']
        sdate1=request.form['sdate1']
        cdate1=request.form['cdate1']
        ptitle2=request.form['ptitle2']
        famount2=request.form['famount2']
        sdate2=request.form['sdate2']
        cdate2=request.form['cdate2']
        ptitle3=request.form['ptitle3']
        famount=request.form['famount']
        sdate3=request.form['sdate3']
        cdate3=request.form['cdate3']
        userid=staffid

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cursor= mysql.connection.cursor()
            cursor.execute('INSERT INTO profile(staffid,name,designation,Department,datefield,address,phone,email,image,degree1,college1,yearpassing1,percentage1,degree2,college2,yearpassing2,percentage2,degree3,college3,yearpassing3,percentage3,course1,cfrom1,cto1,experience1,course2,cfrom2,cto2,experience2,course3,cfrom3,cto3,experience3,AreaofInterest,Achievement,researchtitle1,jc1,pdate1,ni1,researchtitle2,jc2,pdate2,ni2,researchtitle3,jc3,pdate3,ni3,researchtitle4,jc4,pdate4,ni4,ptitle1,famount1,sdate1,cdate1,ptitle2,famount2,sdate2,cdate2,ptitle3,famount,sdate3,cdate3) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(staffid,staffname,designation,Department,datefield,address,phone,email,filename,degree1,college1,yearpassing1,percentage1,degree2,college2,yearpassing2,percentage2,degree3,college3,yearpassing3,percentage3,course1,cfrom1,cto1,experience1,course2,cfrom2,cto2,experience2,course3,cfrom3,cto3,experience3,Areaofinterest,Achievement,researchtitle1,jc1,pdate1,ni1,researchtitle2,jc2,pdate2,ni2,researchtitle3,jc3,pdate3,ni3,researchtitle4,jc4,pdate4,ni4,ptitle1,famount1,sdate1,cdate1,ptitle2,famount2,sdate2,cdate2,ptitle3,famount,sdate3,cdate3))
            mysql.connection.commit()
            cursor.close()
            success='Profile Updated Successfully....!'
            return render_template('user_home.html',userid=userid,success=success)

    else:
        error="Staff Profile Already Exist....!"
        return render_template('user_home.html',userid=userid,error=error)



        


#view profile

@app.route('/view_profile/<string:staffid>')
def view_profile(staffid):
    if staffid:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM profile WHERE staffid=%s",[staffid])
        profile=cursor.fetchone()
        if profile:
            v_profile=profile

            
            
            #image = Image.open(io.BytesIO(binary_data))
            #print(image)
            return render_template('view_profile.html',profile=v_profile)
            mysql.connection.commit()
            cursor.close()
        else:
            error='Please Fill Your Profile....!'
            return render_template('user_home.html',error=error,userid=staffid)




if (__name__ == "__main__"):
    app.run(debug="True",port=8000)

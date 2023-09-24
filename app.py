from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymysql import connections
import os
import boto3
from config import *
import datetime

app = Flask(__name__)
app.secret_key = "Assignment"

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)
output = {}
table = 'Admin', 'Supervisor', 'Student'
studentTable = 'Student'
companyTable = 'Company'

#Home 
@app.route('/')
def Home():
    return render_template('index.html')


# Admin 
@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')

@app.route('/AdminLoginProcess', methods=['POST'])
def AdminLoginProcess():
    login_email = request.form['email']
    login_password = request.form['password']
    
    search_sql = "SELECT * FROM Admin WHERE email=%s AND password=%s"
    
    cursor = db_conn.cursor()
    cursor.execute(search_sql, (login_email,login_password))

    admin = cursor.fetchone()
    cursor.close()  

    if admin:
        session["user"] = admin
        print("Login success")

    else:
        print("Login failed")
        return redirect(url_for('AdminLogin'))

    return redirect(url_for('AdminAdministration'))

@app.route('/AdminAdministration')
def AdminAdministration():
    return render_template('AdminAdministration.html')

@app.route("/AdminAdministration", methods=['POST'])
def AddAdmin():
    if request.method == 'POST': 
      name = request.form['name']
      email = request.form['email']
      contactNum = request.form['contactNum']
      
      insert_sql = "INSERT INTO Admin VALUES (%s, %s, %s)"
      cursor = db_conn.cursor()
      cursor.execute(insert_sql, (name, email, contactNum))
      flash('Admin Added Successfully')
      db_conn.commit()
      cursor.close()

    return render_template('AdminAdministration.html')


# Supervisor 
@app.route('/SupervisorLogin')
def SupervisorLogin():
    return render_template('SupervisorLogin.html')

@app.route("/SupervisorLoginProcess", methods=['POST'])
def SupervisorLoginProcess():
    login_email = request.form['email']
    login_password = request.form['password']
    
    search_sql = "SELECT * FROM Supervisor WHERE email=%s AND password=%s"
    
    cursor = db_conn.cursor()
    cursor.execute(search_sql, (login_email,login_password))

    supervisor = cursor.fetchone()
    cursor.close()  

    if supervisor:
        session["user"] = supervisor
        print("Login success")

    else:
        print("Login failed")
        return redirect(url_for('SupervisorLogin'))

    return redirect(url_for('Supervisor'))

@app.route('/SupervisorAdministration')
def SupervisorAdministration():
    return render_template('SupervisorAdministration.html')

@app.route("/SupervisorAdministration", methods=['POST'])
def AddSupervisor():
    staffID = request.form['staffID']
    name = request.form['name']
    email = request.form['email']
    contactNum = request.form['contactNum']
    
    insert_sql = "INSERT INTO Supervisor VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (staffID, name, email, contactNum))
    flash('Supervisor Added Successfully')
    db_conn.commit()
    cursor.close()

    return render_template('SupervisorAdministration.html')



# Company 
@app.route('/CompanyLogin')
def CompanyLogin():
    return render_template('CompanyLogin.html')

@app.route("/CompanyLoginProcess", methods=['POST'])
def CompanyLoginProcess():
    login_email = request.form['email']
    login_password = request.form['password']
    
    search_sql = "SELECT * FROM Company WHERE email=%s AND password=%s"
    
    cursor = db_conn.cursor()
    cursor.execute(search_sql, (login_email,login_password))

    company = cursor.fetchone()
    cursor.close()  

    if company:
        session["user"] = company
        print("Login success")

    else:
        print("Login failed")
        return redirect(url_for('CompanyLogin'))

    return redirect(url_for('registration'))

@app.route('/CompanyAdministration')
def CompanyAdministration():
    cursor = db_conn.cursor()
    status_approved = 'approved'
    cursor.execute('SELECT * FROM Company WHERE regStatus = %s', status_approved)
    data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyAdministration.html', company = data)

@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def deleteCompany(id):
    cursor = db_conn.cursor()
    cursor.execute('DELETE FROM Company WHERE name = %s', id)
    flash('Company Deleted Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('CompanyAdministration'))

@app.route('/CompanyRegistration')
def CompanyRegistration():
    cursor = db_conn.cursor()
    status_pending = 'pending'
    cursor.execute('SELECT * FROM Company WHERE regStatus = %s', status_pending)
    data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyRegistration.html', company = data)

@app.route('/rejectCompany/<string:name>', methods = ['POST', 'GET'])
def rejectCompany(name):
    cursor = db_conn.cursor()
    status_change = 'rejected'
    cursor.execute("""
            UPDATE Company
            SET regStatus = %s
            WHERE name = %s
        """, (status_change, name))
    flash('Company Rejected Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('CompanyRegistration'))

@app.route('/approveCompany/<string:name>', methods = ['POST', 'GET'])
def approveCompany(name):
    cursor = db_conn.cursor()
    status_change = 'approved'
    cursor.execute("""
            UPDATE Company
            SET regStatus = %s
            WHERE name = %s
        """, (status_change, name))
    flash('Company Approved Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('CompanyRegistration'))

# Student 
@app.route('/StudentRegistration')
def StudentRegistration():
    cursor = db_conn.cursor()
    status_value = 'pending'
    cursor.execute('SELECT * FROM Student WHERE regStatus = %s', status_value)
    data = cursor.fetchall()
    cursor.close()

    return render_template('StudentRegistration.html', student = data)

@app.route('/rejectStudent/<string:id>', methods = ['POST', 'GET'])
def rejectStudent(id):
    cursor = db_conn.cursor()
    status_change = 'rejected'
    cursor.execute("""
            UPDATE Student
            SET regStatus = %s
            WHERE studentID = %s
        """, (status_change, id))
    flash('Student Rejected Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('StudentRegistration'))

@app.route('/approveStudent/<string:id>', methods = ['POST', 'GET'])
def approveStudent(id):
    cursor = db_conn.cursor()
    status_change = 'approved'
    cursor.execute("""
            UPDATE Student
            SET regStatus = %s
            WHERE studentID = %s
        """, (status_change, id))
    flash('Student Approved Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('StudentRegistration'))




# Debbie 
@app.route("/Logout")
def Logout():
    session.pop('user', None)
    flash("Logout succesfully")
    return redirect(url_for('Home'))

@app.route('/StudentLogin')
def StudentLogin():
    return render_template('StudentLogin.html')

@app.route("/StudentSignUp")
def StudentSignUp():
    return render_template('StudentSignUp.html')

@app.route("/Documents")
def Documents():
    if 'user' in session:
        return render_template('Documents.html')
    else:
        return redirect(url_for('StudentLogin'))

@app.route("/Profile")
def Profile():
    if 'user' in session:
        return render_template('Profile.html',user=session["user"])
    else:
        return redirect(url_for('StudentLogin'))
    
@app.route("/UploadDocument", methods=['POST'])
def UploadDocument():
    if 'user' in session:
        userId = session['user'][0]
        userName = session['user'][1]
        userStudentId = session['user'][2]
        resume = request.files['resume-pdf-upload']
        indemnity = request.files['indemnity-pdf-upload']
        company = request.files['company-pdf-upload']
        parent = request.files['parent-pdf-upload']
        cursor = db_conn.cursor()
        insert_sql = "INSERT INTO leave_application (Employee_ID, Submission_Date, Reason_of_Leave, Total_Day) VALUES (%s, %s, %s, %s)"
        #if resume.filename != "":
        try:
            resume_name_in_s3 = userName + "_" + userStudentId + "_resume"
            parent_name_in_s3 = userName + "_" + userStudentId + "_parent"
            indemnity_name_in_s3 = userName + "_" + userStudentId + "_indemnity"
            company_name_in_s3 = userName + "_" + userStudentId + "_company"
            s3 = boto3.resource('s3')

   

            try:
                print('pass0')
                bucket = s3.Bucket(custombucket)

                # Upload objects to the S3 bucket
                bucket.put_object(Key=resume_name_in_s3, Body=resume)
                bucket.put_object(Key=company_name_in_s3, Body=company)
                bucket.put_object(Key=indemnity_name_in_s3, Body=indemnity)
                bucket.put_object(Key=parent_name_in_s3, Body=parent)
                print('pass1')
                bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                s3_location = (bucket_location['LocationConstraint'])
                print('pass2')
                if s3_location is None:
                    s3_location = ''
                else:
                    s3_location = '-' + s3_location

                print('pass3')
                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    resume_name_in_s3)

            except Exception as e:
                return str(e)

        finally:
            cursor.close()

    else:
        return redirect(url_for('Login'))

@app.route("/CompanyDetailsPage/<string:id>")
def CompanyDetailsPage(id):
    cursor = db_conn.cursor()
    getById_sql = "SELECT * FROM Company WHERE id=%s"
    cursor.execute(getById_sql,(id))
    company = cursor.fetchone()
    cursor.close()
    return render_template('CompanyDetailsPage.html',company=company)


@app.route("/ApplyJob/<string:id>")
def ApplyJob(id):
    cursor = db_conn.cursor()
    user = session['user'][0]
    current_date_time = datetime.datetime.now()
    current_date_str = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
    print(user)
    print(id)
    cursor.execute("INSERT INTO StudentApplication(studentName, studentID, date, companyId) VALUES (%s, %s, %s, %s)",(session['user'][1],session['user'][0],current_date_str,id))
    db_conn.commit()
    cursor.close()
    return redirect(url_for('CompanyDetailsPage', id=id))




#functions 
@app.route("/StudentLoginProcess", methods=['POST'])
def StudentLoginProcess():
    login_email = request.form['email']
    login_password = request.form['password']
    
    search_sql = "SELECT * FROM " + studentTable + " WHERE email=%s AND ic=%s"
    
    cursor = db_conn.cursor()
    cursor.execute(search_sql, (login_email,login_password))

    student = cursor.fetchone()
    cursor.close()  

    
    if student:
        if student[17] != 'pending':
            session["user"] = student
            print("Login success")
            return redirect(url_for('Documents'))
        else:
            flash('Account is still pending for approval')

    else:
        print("Invalid Email Address or Password")
        

    return redirect(url_for('StudentLogin'))

@app.route("/StudentSignUpProcess", methods=['POST'])
def StudentSignUpProcess():
    stud_name = request.form['name']
    stud_id = request.form['studentID']
    stud_email= request.form['email']
    stud_ic = request.form['ic']
    stud_contact=request.form['contactNum']
    stud_cgpa = request.form['cgpa']
    stud_programme = request.form['programme']
    stud_group =request.form['group']
    stud_cohort = request.form['cohort']
    stud_ucSupervisor = request.form['ucSupervisor']
    stud_ucEmail = request.form['ucEmail']

    insert_sql = "INSERT INTO " + studentTable + " (studentID, name, email, ic, contactNum, cgpa, programme, tutGroup, cohort, supervisor, supervisorEmail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    try:

        cursor.execute(insert_sql, (stud_id, stud_name, stud_email, stud_ic, stud_contact, stud_cgpa, stud_programme, stud_group, stud_cohort, stud_ucSupervisor, stud_ucEmail))
        db_conn.commit()
    finally:
        cursor.close()
    print("all modification done...")
    return redirect(url_for('StudentLogin')) 

@app.route("/Company")
def Company():
    getAllCompany_sql = "SELECT * FROM " + companyTable 
    
    cursor = db_conn.cursor()
    cursor.execute(getAllCompany_sql)

    companies = cursor.fetchall()
    cursor.close()  

    return render_template('Company.html',companies=companies)


# WanQi 
# Company
@app.route("/Registration", methods=['GET', 'POST'])
def registration():
    return render_template('Registration.html')

@app.route("/AddCompany", methods=['POST'])
def AddCompany():
  
    company_name = request.form['name']
    email = request.form['email']
    contact = request.form['contactNum']
    address = request.form['address']
    company_des = request.form['description']
    work_des = request.form['workDes']
    entry_req = request.form['entryReq']
    image = request.files['company_image_file']
    
    insert_sql = "INSERT INTO Company (name,email,contactNum,address,description,workDes,entryReq,logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    
    object_url = None  # Initialize object_url
    
    if image.filename == "":
        return "Please select a file"
    
    try:
        company_image_file_name_in_s3 = "company-name-" + str(company_name) + "_image_file"
        s3 = boto3.resource('s3')
        print("Data inserted in MariaDB RDS... uploading image to S3...")
        s3.Bucket(custombucket).put_object(Key=company_image_file_name_in_s3, Body=image)
        bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
        s3_location = (bucket_location['LocationConstraint'])

        if s3_location is None:
            s3_location = ''
        else:
            s3_location = '-' + s3_location

        object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
            s3_location,
            custombucket,
            company_image_file_name_in_s3)

    except Exception as e:
        return str(e)   
            
    finally:
        try:
            cursor.execute(insert_sql, (company_name, email, contact, address, company_des, work_des, entry_req, object_url))
            flash('Company Registered Successfully')

            db_conn.commit()

        except Exception as e:
            return str(e)   

        finally:
            cursor.close()
        
    # return redirect(url_for('Jobs'))
    return render_template('Registration.html')
# Job
@app.route("/Jobs", methods=['GET'])
def Jobs():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM Job')
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('Jobs.html', job = data)

@app.route("/CreateJobs", methods=['GET', 'POST'])
def CreateJobs():
    return render_template('CreateJobs.html')

@app.route("/Jobs", methods=['POST'])
def addJob():
    if request.method == 'POST':
        
        job_title = request.form['jobTitle']
        job_location = request.form['jobLocation']
        min_req = request.form['minReq']
        
        # Initialize the cursor
        cursor = db_conn.cursor()
        
        try:         
            print("1")
            insert_sql = "INSERT INTO Job (jobTitle, jobLocation, minReq) VALUES (%s, %s, %s)"
            cursor.execute(insert_sql, (job_title, job_location, min_req))
            db_conn.commit()
            print("yes")
            # Get the auto-generated job_id
            auto_generated_job_id = cursor.lastrowid
        finally:
            cursor.close()
            return redirect(url_for('Jobs'))
        
    # Handle the GET request here
    return render_template('AddJob.html')

#
@app.route("/LoadJob/<int:id>")
def LoadJob(id):
        cursor = db_conn.cursor()
        print(id)
            # Fetch the job details from the database based on the provided 'id'
        cursor.execute('SELECT * FROM Job WHERE jobID = %s', (id))
        job = cursor.fetchone()
        cursor.close()
        if job:
            # Render the edit job form with the fetched job details
            return render_template('EditJob.html', job=job, id=id)
        return render_template('index.html')
        
    


@app.route("/EditJob",methods=['POST'])
def EditJob():

    cursor = db_conn.cursor()
    # Update the job details in the database based on the form submission
    job_id = request.form['jobID']
    job_title = request.form['jobTitle']
    job_location = request.form['jobLocation']
    min_req = request.form['minReq']

    cursor.execute('UPDATE Job SET jobTitle = %s, jobLocation = %s, minReq = %s WHERE jobID = %s',
                    (job_title, job_location, min_req, job_id))
    db_conn.commit()


    cursor.close()

    # Redirect to the jobs page after editing
    return redirect(url_for('Jobs'))



@app.route("/delete/<int:id>", methods=['GET'])
def deleteJob(id):
    cursor = db_conn.cursor()

    # Delete the job from the database based on the provided 'id'
    cursor.execute("DELETE FROM Job WHERE jobID = %s", (id))
    flash('Job Deleted Successfully')
    db_conn.commit()
    cursor.close()

    # Redirect to the jobs page after deleting
    return redirect(url_for('Jobs'))

# Application
@app.route("/Application", methods=['GET'])
def Application():
    cursor = db_conn.cursor()
    status_value = 'pending'
    cursor.execute('SELECT * FROM StudentApplication WHERE appStatus = %s', status_value)
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('Application.html', application = data)

@app.route("/ApplicationStatus", methods=['GET'])
def ApplicationStatus():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM StudentApplication')
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('ApplicationStatus.html', application = data)

@app.route('/rejectStudentApplication/<string:id>', methods = ['POST', 'GET'])
def rejectStudentApplication(id):
    cursor = db_conn.cursor()
    status_change = 'rejected'
    cursor.execute('UPDATE StudentApplication SET appStatus = %s WHERE studentID = %s', (status_change, id))
    flash('Student Application Rejected Successfully')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('Application'))

        

@app.route('/approveStudentApplication/<string:id>', methods = ['POST', 'GET'])
def approveStudentApplication(id):
    cursor = db_conn.cursor()
    status_change = 'approved'
    cursor.execute('UPDATE StudentApplication SET appStatus = %s WHERE studentID = %s', (status_change, id))
    flash('Student Application Approved Successfully', 'success')
    db_conn.commit() 
    cursor.close()
    return redirect(url_for('Application'))
    

#Supervisor
@app.route("/Supervisor")
def Supervisor():
    cursor = db_conn.cursor()
    cursor.execute('SELECT * FROM Student')
    data = cursor.fetchall()
    cursor.close()

    return render_template('Supervisor.html', StudentInfo = data)

@app.route("/Form")
def Form():
    cursor = db_conn.cursor()
    cursor.execute('SELECT name, id FROM Student')
    data = cursor.fetchall()
    cursor.close()

    return render_template('Form.html', StudentInfo=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

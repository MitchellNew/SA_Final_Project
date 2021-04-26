from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql
#sql is an alias for sqlite3
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
#Creating the EmployeePatient database for the application
#conn	=	sql.connect('EmployeePatient.db')
#conn.execute('CREATE	TABLE	IF NOT EXISTS   employees	(EmpID  INTEGER PRIMARY KEY AUTOINCREMENT,  FirstName	TEXT,	LastName	TEXT,	DateHired	TEXT,   DateWorking    TEXT,   Time_In TEXT,   Time_Out    TEXT,	Department  TEXT)')
#conn.execute('CREATE    TABLE   IF NOT EXISTS   patients    (PatientID  INTEGER PRIMARY KEY AUTOINCREMENT,  Patient_FName  text,   Patient_LName   text,   Patient_Status  text,   Procedure   text,    Procedure_Date  TEXT)')
#conn.execute('CREATE    TABLE   IF NOT EXISTS   IT_staff    (ITEmpID INTEGER PRIMARY KEY AUTOINCREMENT, ITEmpFName text, ITEmpLName    text,   position    text)')
#conn.execute('CREATE    TABLE   IF NOT EXISTS   Appointments    (AppointmentID  INTEGER PRIMARY KEY AUTOINCREMENT,    ITEmpID INTEGER NOT NULL,    PatientID   INTEGER NOT NULL,    EmpID   INTEGER NOT NULL, FOREIGN KEY(ITEmpID) REFERENCES IT_staff (ITEmpID), FOREIGN KEY(PatientID) REFERENCES patients (PatientID), FOREIGN KEY(EmpID) REFERENCES employees (EmpID))')
#conn.close()
#Creating addrec route
@app.route("/addrec", methods=["POST"])
def addrec():
    if request.method == "POST":
        FirstName = request.form["fn"]
        LastName = request.form["ln"]
        DateHired = request.form["dh"]
        DateWorking = request.form["dw"]
        Time_In = request.form["ti"]
        Time_Out = request.form["to"]
        Department = request.form["dpt"]

        with sql.connect("EmployeePatient.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO employees (FirstName, LastName, DateHired, DateWorking, Time_In, Time_Out, Department) VALUES (?, ?, ?, ?, ?, ?, ?)", [FirstName, LastName, DateHired, DateWorking, Time_In, Time_Out, Department])
            con.commit()

            return render_template("employee_register.html")
#creating addpatient route
@app.route("/addpatient", methods=["POST"])
def addpatient():
    if request.method == "POST":
        Patient_FName = request.form["pfn"]
        Patient_LName = request.form["pln"]
        Patient_Status = request.form["pst"]
        Procedure = request.form["preq"]
        Procedure_Date = request.form["pd"]

        with sql.connect("EmployeePatient.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO patients   (Patient_FName, Patient_LName, Patient_Status, Procedure, Procedure_Date) VALUES (?, ?, ?, ?, ?)", [Patient_FName, Patient_LName, Patient_Status, Procedure, Procedure_Date])
            con.commit()

            return render_template("patient_register.html")

@app.route('/')
def hello_world():
    return render_template('home.html')

#Creating form pages for Employees and Patients
@app.route('/employee')
def employee_form():
    return render_template('employee.html')

@app.route('/patient')
def patient_form():
    return render_template('patient.html')

@app.route('/employee_register')
def employee_register():
    con = sql.connect('EmployeePatient.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('SELECT * FROM employees')

    rows = cur.fetchall()
    return render_template('employee_register.html', rows = rows)

@app.route('/patient_register')
def patient_register():

    con = sql.connect('EmployeePatient.db')
    con.row_factory = sql.Row #pulls sql data and assigns it to an internal data structure in the website.
    cur = con.cursor()
    cur.execute('SELECT * FROM patients')

    rows = cur.fetchall()
    return render_template('patient_register.html', rows = rows)

if __name__ == "__main__":
    app.run(debug = True)
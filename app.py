import csv
import os
import sqlite3
# import cv2 as cv
import numpy as nu
# import pyzbar.pyzbar as pyzbar (Scanning QR Code)
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import flask_session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, user_tracked_location, input_location_coords, password_check


# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Connecting to database
conn = sqlite3.connect("database.db", timeout=50, check_same_thread=False)
# conn = sqlite3.connect("23Meritall.db", timeout=50, check_same_thread=False)
db = conn.cursor()
try:
    sqliteConnection = sqlite3.connect("database.db")
    # sqliteConnection = sqlite3.connect("23Meritall.db")
    print("Database created and succcessfully connected to SQLite")

    sqlite_select_Query = "select sqlite_version();"
    db.execute(sqlite_select_Query)
    record = db.fetchall()
    print("SQlite database version is: ", record)
except:
    print(f"Error while connecting to sqlite")


# Database one time generating table
'''
db.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, email TEXT, password TEXT)")

db.execute(""" /*hjhj*/
CREATE TABLE colleges(
SrNo DOUBLE,
Colleg VARCHAR(100),
Choice_Code DOUBLE,
Institute VARCHAR(100),
Course_Name VARCHAR(100),
Exam_JEEMHT__CET VARCHAR(100),
Type VARCHAR(100),
Seat_Type VARCHAR(100)
);""")


db.execute(""" /*hjhj*/
CREATE TABLE meritall(
College_Code INT ,  College_Name VARCHAR(200) ,  Branch_Code INT ,  Branch_Name VARCHAR(200) , Branch_pref INT ,  Branch_Status VARCHAR(50) ,  GOPENS_19 INT ,  GOPENH_19 INT , 
GOPENO_19 INT ,  GSCS_19 INT ,  GSCH_19 INT ,  GSCO_19 INT ,  GSTS_19 INT ,  GSTH_19 INT ,  GVJS_19 INT ,  GVJH_19 INT , 
GVJO_19 INT ,  GNT1S_19 INT ,  GNT1H_19 INT ,  GNT1O_19 INT ,  GNT2S_19 INT ,  GNT2H_19 INT ,  GNT2O_19 INT ,  GNT3S_19 INT , 
GNT3H_19 INT ,  GNT3O_19 INT ,  GOBCS_19 INT ,  GOBCH_19 INT ,  GOBCO_19 INT ,  LOPENS_19 INT ,  LOPENH_19 INT ,  LOPENO_19 INT , 
LSCS_19 INT ,  LSCH_19 INT ,  LSCO_19 INT ,  LSTS_19 INT ,  LSTH_19 INT ,  LVJS_19 INT ,  LVJH_19 INT ,  LNT1S_19 INT ,  LNT1H_19 INT , 
LNT2S_19 INT ,  LNT2H_19 INT ,  LOBCS_19 INT ,  LOBCH_19 INT ,  LOBCO_19 INT ,  PWDOPENS_19 INT ,  PWDOPENH_19 INT ,  DEFOPENS_19 INT , 
TFWS_19 INT ,  EWS_19 INT ,  DEFOBCS_19 INT ,  MI_19 INT ,  LNT3S_19 INT ,  LNT3H_19 INT ,  GOPENS_20 INT ,  GOPENH_20 INT ,  GOPENO_20 INT , 
GSCS_20 INT ,  GSCH_20 INT ,  GSCO_20 INT ,  GSTS_20 INT ,  GSTH_20 INT ,  GVJS_20 INT ,  GVJH_20 INT ,  GNT1S_20 INT ,  GNT1H_20 INT ,  GNT1O_20 INT , 
GNT2S_20 INT ,  GNT2H_20 INT ,  GNT2O_20 INT ,  GNT3S_20 INT ,  GNT3H_20 INT ,  GOBCS_20 INT ,  GOBCH_20 INT ,  GOBCO_20 INT ,  LOPENS_20 INT ,  LOPENH_20 INT , 
LOPENO_20 INT ,  LSCS_20 INT ,  LSCH_20 INT ,  LSCO_20 INT ,  LSTS_20 INT ,  LSTH_20 INT ,  LVJS_20 INT ,  LVJH_20 INT ,  LNT1S_20 INT ,  LNT1H_20 INT ,  LNT2S_20 INT , 
LNT2H_20 INT ,  LOBCS_20 INT ,  LOBCH_20 INT ,  LOBCO_20 INT ,  PWDOPENS_20 INT ,  PWDOPENH_20 INT ,  DEFOPENS_20 INT ,  TFWS_20 INT ,  DEFROBCS_20 INT ,  EWS_20 INT , 
DEFRSCS_20 INT ,  MI_20 INT ,  LNT3S_20 INT ,  LNT3H_20 INT ,  GOPENS INT ,  GOPENH INT ,  GOPENO INT ,  GSCS INT ,  GSCH INT ,  GSCO INT ,  GSTS INT ,  GSTH INT ,  GSTO INT , 
GVJS INT ,  GVJH INT ,  GNT1S INT ,  GNT1H INT ,  GNT2S INT ,  GNT2H INT ,  GNT2O INT ,  GNT3S INT ,  GNT3H INT ,  GOBCS INT ,  GOBCH INT ,  GOBCO INT ,  LOPENS INT ,  LOPENH INT , 
LOPENO INT ,  LSCS INT ,  LSCH INT ,  LSCO INT ,  LSTS INT ,  LSTH INT ,  LVJS INT ,  LVJH INT ,  LNT1S INT ,  LNT1H INT ,  LNT2S INT ,  LNT2H INT ,  LOBCS INT ,  LOBCH INT , 
LOBCO INT ,  PWDOPENS INT ,  PWDOPENH INT ,  DEFOPENS INT ,  TFWS INT ,  DEFROBCS INT ,  EWS INT ,  DEFRSCS INT ,  DEFOBCS INT ,  MI INT ,  LNT3S INT ,  GOPENS_22 INT , 
GOPENH_22 INT ,  GOPENO_22 INT ,  GSCS_22 INT ,  GSCH_22 INT ,  GSCO_22 INT ,  GSTS_22 INT ,  GSTH_22 INT ,  GSTO_22 INT ,  GVJS_22 INT ,  GVJH_22 INT ,  GVJO_22 INT , 
GNT1S_22 INT ,  GNT1H_22 INT ,  GNT1O_22 INT ,  GNT2S_22 INT ,  GNT2H_22 INT ,  GNT2O_22 INT ,  GNT3S_22 INT ,  GNT3H_22 INT ,  GOBCS_22 INT ,  GOBCH_22 INT ,  GOBCO_22 INT , 
LOPENS_22 INT ,  LOPENH_22 INT ,  LOPENO_22 INT ,  LSCS_22 INT ,  LSCH_22 INT ,  LSCO_22 INT ,  LSTS_22 INT ,  LSTH_22 INT ,  LVJS_22 INT ,  LVJH_22 INT ,  LNT1S_22 INT , 
LNT1H_22 INT ,  LNT2S_22 INT ,  LNT2H_22 INT ,  LOBCS_22 INT ,  LOBCH_22 INT ,  LOBCO_22 INT ,  PWDOPENS_22 INT ,  PWDOPENH_22 INT ,  DEFOPENS_22 INT ,  TFWS_22 INT , 
DEFROBCS_22 INT ,  EWS_22 INT ,  PWDROBC_22 INT ,  DEFRSCS_22 INT ,  DEFOBCS_22 INT ,  MI_22 INT ,  LNT3S_22 INT ,  GOPENS_23 INT ,  GOPENH_23 INT ,  GOPENO_23 INT , 
GSCS_23 INT ,  GSCH_23 INT ,  GSCO_23 INT ,  GSTS_23 INT ,  GSTH_23 INT ,  GVJS_23 INT ,  GVJH_23 INT ,  GNT1S_23 INT ,  GNT1H_23 INT ,  GNT2S_23 INT ,  GNT2H_23 INT , 
GNT2O_23 INT ,  GNT3S_23 INT ,  GNT3H_23 INT ,  GOBCS_23 INT ,  GOBCH_23 INT ,  GOBCO_23 INT ,  LOPENS_23 INT ,  LOPENH_23 INT ,  LOPENO_23 INT ,  LSCS_23 INT ,  LSCH_23 INT , 
LSCO_23 INT ,  LSTS_23 INT ,  LSTH_23 INT ,  LVJS_23 INT ,  LVJH_23 INT ,  LNT1S_23 INT ,  LNT1H_23 INT ,  LNT2S_23 INT ,  LNT2H_23 INT ,  LOBCS_23 INT , 
LOBCH_23 INT ,  LOBCO_23 INT ,  PWDOPENS_23 INT ,  PWDOPENH_23 INT ,  DEFOPENS_23 INT ,  TFWS_23 INT
);""")


# Loading colleges info in SQLite table


with open('23meritall.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['College_Code'], i['College_Name'], i['Branch_Code'], i['Branch_Name'], i['Branch_pref'], i['Branch_Status'], i['GOPENS_19'],
              i['GOPENH_19'], i['GOPENO_19'], i['GSCS_19'], i['GSCH_19'], i['GSCO_19'], i['GSTS_19'], i['GSTH_19'], i['GVJS_19'],
              i['GVJH_19'], i['GVJO_19'], i['GNT1S_19'], i['GNT1H_19'], i['GNT1O_19'], i['GNT2S_19'], i['GNT2H_19'], i['GNT2O_19'],
              i['GNT3S_19'], i['GNT3H_19'], i['GNT3O_19'], i['GOBCS_19'], i['GOBCH_19'], i['GOBCO_19'], i['LOPENS_19'], i['LOPENH_19'],
              i['LOPENO_19'], i['LSCS_19'], i['LSCH_19'], i['LSCO_19'], i['LSTS_19'], i['LSTH_19'], i['LVJS_19'], i['LVJH_19'], i['LNT1S_19'],
              i['LNT1H_19'], i['LNT2S_19'], i['LNT2H_19'], i['LOBCS_19'], i['LOBCH_19'], i['LOBCO_19'], i['PWDOPENS_19'], i['PWDOPENH_19'],
              i['DEFOPENS_19'], i['TFWS_19'], i['EWS_19'], i['DEFOBCS_19'], i['MI_19'], i['LNT3S_19'], i['LNT3H_19'], i['GOPENS_20'],
              i['GOPENH_20'], i['GOPENO_20'], i['GSCS_20'], i['GSCH_20'], i['GSCO_20'], i['GSTS_20'], i['GSTH_20'], i['GVJS_20'],
              i['GVJH_20'], i['GNT1S_20'], i['GNT1H_20'], i['GNT1O_20'], i['GNT2S_20'], i['GNT2H_20'], i['GNT2O_20'], i['GNT3S_20'],
              i['GNT3H_20'], i['GOBCS_20'], i['GOBCH_20'], i['GOBCO_20'], i['LOPENS_20'], i['LOPENH_20'], i['LOPENO_20'], i['LSCS_20'],
              i['LSCH_20'], i['LSCO_20'], i['LSTS_20'], i['LSTH_20'], i['LVJS_20'], i['LVJH_20'], i['LNT1S_20'], i['LNT1H_20'],
              i['LNT2S_20'], i['LNT2H_20'], i['LOBCS_20'], i['LOBCH_20'], i['LOBCO_20'], i['PWDOPENS_20'], i['PWDOPENH_20'],
              i['DEFOPENS_20'], i['TFWS_20'], i['DEFROBCS_20'], i['EWS_20'], i['DEFRSCS_20'], i['MI_20'], i['LNT3S_20'],
              i['LNT3H_20'], i['GOPENS'], i['GOPENH'], i['GOPENO'], i['GSCS'], i['GSCH'], i['GSCO'], i['GSTS'], i['GSTH'],
              i['GSTO'], i['GVJS'], i['GVJH'], i['GNT1S'], i['GNT1H'], i['GNT2S'], i['GNT2H'], i['GNT2O'], i['GNT3S'], i['GNT3H'],
              i['GOBCS'], i['GOBCH'], i['GOBCO'], i['LOPENS'], i['LOPENH'], i['LOPENO'], i['LSCS'], i['LSCH'], i['LSCO'], i['LSTS'],
              i['LSTH'], i['LVJS'], i['LVJH'], i['LNT1S'], i['LNT1H'], i['LNT2S'], i['LNT2H'], i['LOBCS'], i['LOBCH'], i['LOBCO'],
              i['PWDOPENS'], i['PWDOPENH'], i['DEFOPENS'], i['TFWS'], i['DEFROBCS'], i['EWS'], i['DEFRSCS'], i['DEFOBCS'], i['MI'],
              i['LNT3S'], i['GOPENS_22'], i['GOPENH_22'], i['GOPENO_22'], i['GSCS_22'], i['GSCH_22'], i['GSCO_22'], i['GSTS_22'],
              i['GSTH_22'], i['GSTO_22'], i['GVJS_22'], i['GVJH_22'], i['GVJO_22'], i['GNT1S_22'], i['GNT1H_22'], i['GNT1O_22'],
              i['GNT2S_22'], i['GNT2H_22'], i['GNT2O_22'], i['GNT3S_22'], i['GNT3H_22'], i['GOBCS_22'], i['GOBCH_22'], i['GOBCO_22'],
              i['LOPENS_22'], i['LOPENH_22'], i['LOPENO_22'], i['LSCS_22'], i['LSCH_22'], i['LSCO_22'], i['LSTS_22'], i['LSTH_22'], i['LVJS_22'],
              i['LVJH_22'], i['LNT1S_22'], i['LNT1H_22'], i['LNT2S_22'], i['LNT2H_22'], i['LOBCS_22'], i['LOBCH_22'], i['LOBCO_22'],
              i['PWDOPENS_22'], i['PWDOPENH_22'], i['DEFOPENS_22'], i['TFWS_22'], i['DEFROBCS_22'], i['EWS_22'], i['PWDROBC_22'],
              i['DEFRSCS_22'], i['DEFOBCS_22'], i['MI_22'], i['LNT3S_22'], i['GOPENS_23'], i['GOPENH_23'], i['GOPENO_23'],
              i['GSCS_23'], i['GSCH_23'], i['GSCO_23'], i['GSTS_23'], i['GSTH_23'], i['GVJS_23'], i['GVJH_23'], i['GNT1S_23'],
              i['GNT1H_23'], i['GNT2S_23'], i['GNT2H_23'], i['GNT2O_23'], i['GNT3S_23'], i['GNT3H_23'], i['GOBCS_23'], i['GOBCH_23'],
              i['GOBCO_23'], i['LOPENS_23'], i['LOPENH_23'], i['LOPENO_23'], i['LSCS_23'], i['LSCH_23'], i['LSCO_23'], i['LSTS_23'],
              i['LSTH_23'], i['LVJS_23'], i['LVJH_23'], i['LNT1S_23'], i['LNT1H_23'], i['LNT2S_23'], i['LNT2H_23'],
              i['LOBCS_23'], i['LOBCH_23'], i['LOBCO_23'], i['PWDOPENS_23'], i['PWDOPENH_23'], i['DEFOPENS_23'], i['TFWS_23']) for i in dr]
db.executemany("""INSERT INTO meritall (College_Code , College_Name , Branch_Code , Branch_Name, Branch_pref , Branch_Status , GOPENS_19 , GOPENH_19 , GOPENO_19 , 
               GSCS_19 , GSCH_19 , GSCO_19 , GSTS_19 , GSTH_19 , GVJS_19 , GVJH_19 , GVJO_19 , GNT1S_19 , GNT1H_19 , GNT1O_19 , GNT2S_19 , GNT2H_19 , 
               GNT2O_19 , GNT3S_19 , GNT3H_19 , GNT3O_19 , GOBCS_19 , GOBCH_19 , GOBCO_19 , LOPENS_19 , LOPENH_19 , LOPENO_19 , LSCS_19 , LSCH_19 , 
               LSCO_19 , LSTS_19 , LSTH_19 , LVJS_19 , LVJH_19 , LNT1S_19 , LNT1H_19 , LNT2S_19 , LNT2H_19 , LOBCS_19 , LOBCH_19 , LOBCO_19 , PWDOPENS_19 , 
               PWDOPENH_19 , DEFOPENS_19 , TFWS_19 , EWS_19 , DEFOBCS_19 , MI_19 , LNT3S_19 , LNT3H_19 , GOPENS_20 , GOPENH_20 , GOPENO_20 , GSCS_20 , 
               GSCH_20 , GSCO_20 , GSTS_20 , GSTH_20 , GVJS_20 , GVJH_20 , GNT1S_20 , GNT1H_20 , GNT1O_20 , GNT2S_20 , GNT2H_20 , GNT2O_20 , GNT3S_20 , 
               GNT3H_20 , GOBCS_20 , GOBCH_20 , GOBCO_20 , LOPENS_20 , LOPENH_20 , LOPENO_20 , LSCS_20 , LSCH_20 , LSCO_20 , LSTS_20 , LSTH_20 , LVJS_20 , 
               LVJH_20 , LNT1S_20 , LNT1H_20 , LNT2S_20 , LNT2H_20 , LOBCS_20 , LOBCH_20 , LOBCO_20 , PWDOPENS_20 , PWDOPENH_20 , DEFOPENS_20 , TFWS_20 , 
               DEFROBCS_20 , EWS_20 , DEFRSCS_20 , MI_20 , LNT3S_20 , LNT3H_20 , GOPENS , GOPENH , GOPENO , GSCS , GSCH , GSCO , GSTS , GSTH , GSTO , GVJS , 
               GVJH , GNT1S , GNT1H , GNT2S , GNT2H , GNT2O , GNT3S , GNT3H , GOBCS , GOBCH , GOBCO , LOPENS , LOPENH , LOPENO , LSCS , LSCH , LSCO , LSTS , 
               LSTH , LVJS , LVJH , LNT1S , LNT1H , LNT2S , LNT2H , LOBCS , LOBCH , LOBCO , PWDOPENS , PWDOPENH , DEFOPENS , TFWS , DEFROBCS , EWS , DEFRSCS , 
               DEFOBCS , MI , LNT3S , GOPENS_22 , GOPENH_22 , GOPENO_22 , GSCS_22 , GSCH_22 , GSCO_22 , GSTS_22 , GSTH_22 , GSTO_22 , GVJS_22 , GVJH_22 , 
               GVJO_22 , GNT1S_22 , GNT1H_22 , GNT1O_22 , GNT2S_22 , GNT2H_22 , GNT2O_22 , GNT3S_22 , GNT3H_22 , GOBCS_22 , GOBCH_22 , GOBCO_22 , LOPENS_22 , 
               LOPENH_22 , LOPENO_22 , LSCS_22 , LSCH_22 , LSCO_22 , LSTS_22 , LSTH_22 , LVJS_22 , LVJH_22 , LNT1S_22 , LNT1H_22 , LNT2S_22 , LNT2H_22 , 
               LOBCS_22 , LOBCH_22 , LOBCO_22 , PWDOPENS_22 , PWDOPENH_22 , DEFOPENS_22 , TFWS_22 , DEFROBCS_22 , EWS_22 , PWDROBC_22 , DEFRSCS_22 , 
               DEFOBCS_22 , MI_22 , LNT3S_22 , GOPENS_23 , GOPENH_23 , GOPENO_23 , GSCS_23 , GSCH_23 , GSCO_23 , GSTS_23 , GSTH_23 , GVJS_23 , 
               GVJH_23 , GNT1S_23 , GNT1H_23 , GNT2S_23 , GNT2H_23 , GNT2O_23 , GNT3S_23 , GNT3H_23 , GOBCS_23 , GOBCH_23 , GOBCO_23 , LOPENS_23 , 
               LOPENH_23 , LOPENO_23 , LSCS_23 , LSCH_23 , LSCO_23 , LSTS_23 , LSTH_23 , LVJS_23 , LVJH_23 , LNT1S_23 , LNT1H_23 , LNT2S_23 , LNT2H_23 , 
               LOBCS_23 , LOBCH_23 , LOBCO_23 , PWDOPENS_23 , PWDOPENH_23 , DEFOPENS_23 , TFWS_23) 
               VALUES (? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , 
               ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?);""", to_db)
conn.commit()
print("MeritAll insertion successfull")'''


# APP ROUTES

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If user reached route via POST
    if request.method == "POST":
        # Getting info
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check whether password is strong enough
        x = password_check(password)
        if x is False:
            return apology("Please satisfy password requirements")

        # Checking if password equal to confirmation
        if not password == confirmation:
            return apology("Password and confirmation didnt matched")

        # Generating hash to store in database
        hash = generate_password_hash(password)

        # Storing in database
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", [
                   name, email, hash])
        # print("tables interior: ")
        db.execute("SELECT * FROM users")
        # print(f"fetch of register", db.fetchall())

        return redirect("/login")

    # If user reached route via GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If user reached route via POST
    if request.method == "POST":
        # Forget any previous user

        # Getting info
        name = request.form.get("name")
        password = request.form.get("password")

        # Validating info with database
        db.execute("SELECT * FROM users")
        rows = db.fetchall()
        # print(f"fetch of login: {rows}")
        for row in rows:
            if row[1] == name:
                # Remember which user has logged in
                #session["id"] = rows[0][0]
                print("successfull login")
                return redirect("/details")
        return apology("Please register if you havent")

    # If user reached route via GET
    else:
        return render_template("login.html")


@app.route("/details", methods=["GET", "POST"])
def details():
    # If user reached route via POST
    if request.method == "POST":
        # Getting user info
        cet = request.form.get("cet")
        category = request.form.get("category")
        # Location tracking using ip address
        location = request.form.get("location")
        entered_location = request.form.get("entered_location")
        branch = request.form.get("Branch")
        if cet == "":
            return apology("Atleast one marks are required")

        if location == "enter":
            # Find and use API
            print(f"Users entered location is: {entered_location}")
        elif location == "track":
            userlocation = user_tracked_location()
            # print(f"Your current location is: {userlocation}")
        else:
            return apology("please provide location")

        cet = int(cet)+10000
        cet = str(cet)
        # if(int(cet) < 40000):
        #     cet_min = str(max(60, int(cet)-12000))
        # else:
        #     cet_min = str(max(60, int(cet)-25000))
        cet_min = str(60)

        # quary = str('SELECT DISTINCT College_Name,Branch_Name,Branch_Code,Branch_Status,'+category+'S_23,'+category+'H_23,'+category+'O_23 FROM meritall WHERE (('+category+'S_23 >=60 AND '+category+'S_23 <='+cet+') OR ('+category+'H_23 >=60 AND '+category+'H_23 <='+cet+') OR ('+category+'O_23 >=60 AND '+category+'O_23 <='+cet+'))AND Branch_pref LIKE '+branch+' ORDER BY '+category+'S_23 ,'+category+'H_23 ,'+category+'O_23')

        quary = str('SELECT DISTINCT College_Name,Branch_Name,Branch_Code,Branch_Status,'+category+'S_23,'+category+'H_23,'+category+'S_22,'+category+'H_22 FROM meritall WHERE (('+category+'S_23 >='+cet_min+' AND ' + category+'S_23 <='+cet+') OR ('+category+'H_23 >=' +
                    cet_min+' AND '+category+'H_23 <='+cet+') OR ('+category+'S_22 >='+cet_min+' AND ' + category+'S_22 <='+cet+') OR ('+category+'H_22 >='+cet_min+' AND '+category+'H_22 <='+cet+') ) AND Branch_pref LIKE '+branch+' ORDER BY '+category+'H_23,'+category+'S_23')

        db.execute(quary)
        global clg_list
        clg_list = db.fetchall()

        return redirect("/suggestions")
    # If user reached route via GET
    else:
        return render_template("details.html")


@app.route("/suggestions")
def suggestions():
    # Rendering suggestions along with clg list generated in runtime
    return render_template("suggestions.html", clg_list=clg_list)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    # If user reached route via POST
    if request.method == "POST":
        # Getting user info
        cet = request.form.get("cet")
        category = request.form.get("category")
        # Location tracking using ip address
        location = request.form.get("location")
        entered_location = request.form.get("entered_location")
        branch = request.form.get("Branch")
        if cet == "":
            return apology("Atleast one marks are required")

        if location == "enter":
            # Find and use API
            print(f"Users entered location is: {entered_location}")
        elif location == "track":
            userlocation = user_tracked_location()
            # print(f"Your current location is: {userlocation}")
        else:
            return apology("please provide location")

        cet = int(cet)+10000
        cet = str(cet)
        # if(int(cet) < 40000):
        #     cet_min = str(max(60, int(cet)-12000))
        # else:
        #     cet_min = str(max(60, int(cet)-25000))
        cet_min = str(60)
        # quary = str('SELECT DISTINCT College_Name,Branch_Name,Branch_Code,Branch_Status,'+category+'S_23,'+category+'H_23,'+category+'O_23 FROM meritall WHERE (('+category+'S_23 >=60 AND '+category+'S_23 <='+cet+') OR ('+category+'H_23 >=60 AND '+category+'H_23 <='+cet+') OR ('+category+'O_23 >=60 AND '+category+'O_23 <='+cet+'))AND Branch_pref LIKE '+branch+' ORDER BY '+category+'S_23 ,'+category+'H_23 ,'+category+'O_23')

        quary = str('SELECT DISTINCT College_Name,Branch_Name,Branch_Code,Branch_Status,'+category+'S_23,'+category+'H_23,'+category+'S_22,'+category+'H_22 FROM meritall WHERE (('+category+'S_23 >='+cet_min+' AND ' + category+'S_23 <='+cet+') OR ('+category+'H_23 >=' +
                    cet_min+' AND '+category+'H_23 <='+cet+') OR ('+category+'S_22 >='+cet_min+' AND ' + category+'S_22 <='+cet+') OR ('+category+'H_22 >='+cet_min+' AND '+category+'H_22 <='+cet+') ) AND Branch_pref LIKE '+branch+' ORDER BY '+category+'H_23,'+category+'S_23')
        db.execute(quary)
        global clg_list
        clg_list = db.fetchall()

        return redirect("/prediction")
    # If user reached route via GET
    else:
        return render_template("predict.html")


@app.route("/prediction")
def prediction():
    # Rendering suggestions along with clg list generated in runtime
    return render_template("prediction.html", clg_list=clg_list)


@app.route("/CollegeCutoff", methods=["GET", "POST"])
def CollegeCutoff():
    # If user reached route via POST
    if request.method == "POST":
        Institute = request.form.get("Institute")
        Institute = str(Institute)
        category = request.form.get("category")
        college_branch = request.form.get("Branch")

        # print(Institute)
        # print(str('"'+Institute+'"'))
        # print(Institute)

        quary = str('SELECT DISTINCT College_Name,Branch_Name,Branch_Code,Branch_Status,'+category+'S_23,'+category+'S_22, '+category +
                    'H_23 ,'+category+'H_22 FROM meritall WHERE College_Name LIKE '+str('"'+Institute+' "')+'AND Branch_pref LIKE '+college_branch+' ')

        db.execute(quary)
        global clg_M_list
        clg_M_list = db.fetchall()
        print(clg_M_list[0])

        return redirect("CMPrediction")
    # If user reached route via GET
    else:
        return render_template("CollegeCutoff.html")


@app.route("/CMPrediction")
def CMPrediction():
    # Rendering suggestions along with clg list generated in runtime
    return render_template("CMPrediction.html", clg_M_list=clg_M_list)

# Error handlers


def errorhandler(e):
    # Basic error handeling
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0',port=8000)
    app.run(debug=True)

conn.close()

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy#pyscopg2 - sends sql statements to database, sqlAchemy - Higher level than psycopg2 - Dont need to connect and commit every time
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
db=SQLAlchemy()
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector' #postgresql://username:password@localhost/db_name
app.config['SQLALCHEMY_DATABASE_URI']='postgres://immjeouexczkix:770d2618c3dce0a0c7cabae633e8d40547021a473bb77606bb102acbdd1c9c3f@ec2-3-224-165-85.compute-1.amazonaws.com:5432/dd43t5utjg9mmu?sslmode=require'
db=SQLAlchemy(app)

class Data(db.Model): #Accessing Model class of SQLAlchemy object
    __tablename__="data" #creating table
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=="POST":#Sometimes we also get GET requests
        email=request.form["email_id"]
        height=request.form["height"]

        if db.session.query(Data).filter(Data.email_==email).count() ==0:
            data=Data(email,height)#data is not the name of the table
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count = db.session.query(Data.height_).count()
            send_email(email,height,average_height,count)
            return render_template("success.html")
    return render_template("index.html",text="Email already exists!")
if __name__=="__main__":
    app.debug=True
    app.run()

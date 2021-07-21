from re import search
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import sys
import os
p = os.path.abspath('.')
sys.path.insert(1, p)
from setting import * 

#sys.a
import Ebay_scapper as ES
import datetime

TODAYSDATE=str(datetime.datetime.today().date()).replace("-","")


app = Flask(__name__,static_folder="static")
#SQLの設定
app.config['SQLALCHEMY_DATABASE_URL']=DATABESE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db=SQLAlchemy(app)
#https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/patterns/sqlalchemy.html
#db= scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=ENGINE))
#Base = declarative_base()
#Base.query = db.query_property()

class Search(db.Model):
    
   __tablename__ = "serach_history"
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   searchname= db.Column(db.Text())
   URL=db.Column(db.Text())
   PIC=db.Column(db.Text())
   pagenum=db.Column(db.Integer)
   searchdate=db.Column(db.Date)
   status = db.Column(db.Integer)
   datapoints=db.Column(db.Integer)
   

  # soldstatus=db.Column(db.Boolean, server_default=False, nullable=False)
  # status=db.Column(db.Boolean, server_default=False, nullable=False)
   
db.create_all()
"""
def __init__(self) -> None:
    super().__init__()

def _search(self,searchname,pageitmes,pagenum,msold):
    URL=ES.createUrl(searchname,pageitems=pageitems,sold=sold)
    browser=ES.start_browser()
    Data=ES.Ebay_MarketData(URL,pagenum,browser,sold=sold)
__tablename__ = f"{TODAYSDATE}_{title}_{len(Data)}"
"""

@app.route('/add',methods=["POST"])
def add():
   
    search=Search()
    search.searchname=request.form["searchname"]
    search.searchdate=datetime.datetime.today().date()
    search.pagenum=request.form["pagenumbers"]
   # if request.form["Sold"]=="on":
    #    search.soldtype=True
    #else:
    search.soldtype=False
    search.URL=ES.createUrl(search.searchname,n=None,pageitems=50,sold=search.soldtype)
    search.status = 0
    search.databasetitle=""

    #Runsuch
    browser=ES.start_browser()
    Data=ES.Ebay_MarketData(search.URL,int(search.pagenum),browser,sold=search.soldtype)
    

    #Save data to SQL 
    title_database=f"{search.searchname.replace(' ','')}_RESULTS_{TODAYSDATE}_{search.soldtype}"
    
    Data.to_sql(f"{title_database}",con=ENGINE, if_exists="replace")
    #Databse update
    search.databasetitle=title_database
    search.status = 1

    db.session.add(search)
    db.session.commit()



    return redirect(url_for("index"))



@app.route("/runsearch",methods=["POST"])
def runsearch():
    id = request.form["id"]
    search = Search.query.filter_by(id=id).first()
    search= search.URL
    browser=ES.start_browser()
    Data=ES.Ebay_MarketData(search.URL,search.pagenum,browser,sold=search.soldtype)
    

    #Save data to SQL 
    title_database=f"{search.searchname.replace(' ','')}_RESULTS_{TODAYSDATE}_{search.soldtype}"
    Data.to_sql(f"{title_database}",con=ENGINE, if_exists="replace")
    #Databse update
    search.databasetitle=title_database
    search.status = 1
    db.session.commit()
    return redirect(url_for("index"))




@app.route('/')
def index():
    searchs = Search.query.all()
    return render_template('index.html',searchs=searchs)



db.create_all()
app.run(debug=True, host=os.getenv('APP_ADDRESS', 'localhost'))

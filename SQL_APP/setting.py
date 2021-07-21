from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base



DATABASE_CONFIG={
   "user":"postgres",
   "password":"{pw}",
   "host":"127.0.0.1",
   "port":"{port}",
   "database":"Ebay_scrapper",
}

DATABESE_URL='postgresql://{user}:{password}@{host}:{port}/{database}'.format(**DATABASE_CONFIG)

ENGINE=create_engine(DATABESE_URL)

session = scoped_session(
    sessionmaker(
        autocommit= False, 
        autoflush=False,
        bind=ENGINE
    )
)

Base= declarative_base()
Base.query = session.query_property()

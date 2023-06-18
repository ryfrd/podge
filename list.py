from db import Episode

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from time import time, strftime, localtime

engine = create_engine('sqlite:///podcasts.db')
Session = sessionmaker(bind=engine)
session = Session()

# query db for episodes
# filter for age (in days)
# orde by age
# print info

def sort_by_age(x):
    return x.time
    
def pretty_list(age):
    db_eps = session.query(Episode)
    approved_eps = []
    for ep in db_eps:
        if ep.time > (time() - (age * 86400)):
            approved_eps.append(ep)
    approved_eps.sort(key=sort_by_age,reverse=True)
            
    for ep in approved_eps:
        title = ep.title
        date = strftime('%d/%m/%Y', localtime(ep.time))
        podcast = ep.podcast.name
        print(f'{title} ~ {podcast} ~ {date}')

pretty_list(4)
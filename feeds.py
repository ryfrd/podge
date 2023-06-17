from db import Podcast, Episode

from feedparser import parse
from time import time, mktime, strftime, localtime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///podcasts.db')
Session = sessionmaker(bind=engine)
session = Session()

def is_duplicate(title, time, url):
    existing_episode = session.query(Episode).filter_by(
        title=title,
        time=time,
        content_url=url
    ).first()
    return existing_episode is not None

# get rss feeds from db
# parse feeds
# check if duplicate
# write episode info to db
def parse_feeds():
    podcasts = session.query(Podcast).all()
    for podcast in podcasts:
        f = parse(podcast.rss_feed)
        for episode in f.entries:

            title = episode.title
            time = mktime(episode.published_parsed)
            url = episode.enclosures[0].href

            new_episode = Episode(
                title = title,
                time = time,
                content_url = url,
                podcast_id = session.query(Podcast).filter_by(name = podcast.name).first().id
            )

            if is_duplicate(title, time, url):
                pass
            else:
                session.add(new_episode)
                session.commit()
                print(episode.title, 'from', podcast.name)


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

# parse_feeds()
pretty_list(7)




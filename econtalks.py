# coding: utf-8
from bs4 import BeautifulSoup
import requests as requests
import time

BASE_URL = 'http://www.econtalk.org/archives.html'

def timestamp(e):
    date = e.select('.dateline')[0].getText().split('|')[-1].strip()
    dt = time.strptime(date, "%B %d, %Y")
    timestamp = "%d.%02d.%02d" % (dt.tm_year, dt.tm_mon, dt.tm_mday)
    return timestamp

def title(e):
    return e.select('h1.title')[0].string

r = requests.get('http://www.econtalk.org/archives.html')

soup = BeautifulSoup(r.text)

talks = soup.select('.archive tr td a[href$=".html"]')

for talk in talks:
    r = requests.get(talk['href'])
    if r.status_code == 200:
        e = BeautifulSoup(r.text)
        url = e.select('a[href$="mp3"]')
        if len(url) > 1:
            url = url[1]['href']
            q = requests.get(url, stream=True)
            ts = timestamp(e)
            t = title(e)
            fn = "%s - %s.mp3" % (ts, t)
            print fn
            with open(fn, 'wb') as f:
                for chunk in q.iter_content(1024):
                    f.write(chunk)
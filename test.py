import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import os.path

DB_NAME = 'parser.db'
LINK = 'https://www.work-nest.com/jobs/'

class Job:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

        c = self.conn.cursor()
        c.execute('drop table if exists vacancy;')

        c.execute(
            'create table vacancy '
            '(title text, city text, offer text, about text);'
        )
    def parse(self, careers_url, view=None):
        r = requests.get(careers_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        elements = soup.find_all('section', class_='opening-section-2')

        for name in elements:
            title = name.find('h3',class_='section-title').get_text()

            city = name.find('div',class_='opening-info-item-details').get_text()

            offer = name.find('div',class_='col-md-auto').find('ul').get_text()

            p = name.find('div',class_='col-md-auto').find('p')
            if p:
                about = p.get_text()
            else:
                about = ''

            if ((view is not None) and (view == True)):
                print('Title: ' + title)
                print('City: ' + city)
                print('Offer: ' + offer)
                print('About: ' + about)
                print('_______________________________________________________')

            c = self.conn.cursor()
            c.execute(
                'insert into vacancy (title, city, offer, about) '
                'values (?, ?, ?, ?)',
                (title, city, offer, about)
            )
            self.conn.commit()

def main():
    job = Job(db_name=DB_NAME)
    job.parse(careers_url=LINK,view=True)

if __name__ == '__main__':
    main()

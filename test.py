import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
import os.path

class Job(object):
    Title = ""
    City = ""
    Offer = ""
    About_project = ""

def get_html(url):
    r = requests.get(url)
    return r.text #return HTML-code page (url)

#parse all vacancy
def get_items(html):
    soup = BeautifulSoup(html, 'html.parser')

    ement = soup.find_all('section', class_='opening-section-2') #find all tags witg name 'section' and class 'opening-section-2'

    names = [] #variable all titles opening job
    for name in ement:
        obj_job = Job()
        a = name.find('h3',class_='section-title')

        obj_job.Title = a.get_text()

        obj_job.City = name.find('div',class_='opening-info-item-details').get_text()

        obj_job.Offer = name.find('div',class_='col-md-auto').find('ul').get_text()
        try:
            obj_job.About_project = name.find('div',class_='col-md-auto').find('p').get_text()
        except Exception as e:
            obj_job.About_project = ''

        names.append(obj_job)
    return names

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        conn.close()

def sql_base():
    conn = sqlite3.connect("siteWorkNest.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""CREATE TABLE Jobs
                      (Title text, City text, Offer text,
                       About_project text)
                   """)

def add_row(title,city,offer,about):
    conn = sqlite3.connect("siteWorkNest.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    query = "INSERT INTO Jobs VALUES ('" + title + "', '" + city + "', '" + offer + "', '" + about + "')"

    # Вставляем данные в таблицу
    cursor.execute(query)

    # Сохраняем изменения
    conn.commit()

def view_base():
    conn = sqlite3.connect("siteWorkNest.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT * FROM Jobs"
    cursor.execute(sql)
    print(cursor.fetchall()) # or use fetchone()

def clear_table():
    conn = sqlite3.connect("siteWorkNest.db")
    cursor = conn.cursor()

    sql = "delete from Jobs"
    cursor.execute(sql)

def view_vacance(selCity):
    ements = get_items(get_html('https://www.work-nest.com/jobs/'))
    if selCity == 'all':
        for i in ements:
            print('Job: ' + i.Title)
            print('City: ' + i.City)
            print('We are ready to offer: ' + i.Offer)
            print('About the project: ' + i.About_project)
    else:
        for i in ements:
            if i.City.find(selCity) > -1:
                print('Job: ' + i.Title)
                print('City: ' + i.City)
                print('We are ready to offer: ' + i.Offer)
                print('About the project: ' + i.About_project)


def main():
    isWork = True
    while isWork:
        print('1. View all vacancy')
        print('2. View vacancy Kharkiv')
        print('3. View vacancy Kyiv')
        print('4. View vacancy Remote')
        print('5. Write all vacancy in SQLite')
        choice = input('Select option:')

        if choice == '1' or choice == 1:
            view_vacance('all')
        else:
            if choice == '2' or choice == 2:
                view_vacance('Kharkiv')
            else:
                if choice == '3' or choice == 3:
                    view_vacance('Kyiv')
                else:
                    if choice == '4' or choice == 4:
                        view_vacance('Remote')
                    else:
                        if choice == '5' or choice == 5:
                            ements = get_items(get_html('https://www.work-nest.com/jobs/'))

                            if os.path.exists('siteWorkNest.db'):
                                clear_table()
                                for i in ements:
                                    add_row(i.Title,i.City,i.Offer,i.About_project)
                            else:
                                create_connection('siteWorkNest.db')
                                sql_base()
                                for i in ements:
                                    add_row(i.Title,i.City,i.Offer,i.About_project)


        choice = input('Exit [y/n]: ')
        if choice == 'y':
            isWork = False
        pass

if __name__ == '__main__':
    main()

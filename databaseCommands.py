#!/usr/bin/python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
#app = Flask(__name__)
from backend import db, app
class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))

    def __init__(self, password, email, firstName, lastName):
        self.password = password
        self.email = email
        self.firstName = firstName
        self.lastName = lastName

    def create_user(self):
        status = Users.query.filter_by(email=self.email).first()
        if status is not None:
            return False
        db.session.add(self)
        db.session.commit()
        return True

    def login_user(self):
        account = Users.query.filter_by(email=self.email).first()
        if account is None:
            return False
        elif self.password != account.password:
            return False
        else:
            self.firstName = account.firstName
            self.lastName = account.lastName
            self.user_id = account.user_id
            return True

'''class Notebooks(db.Model):
    __tablename__ = 'Notebooks'
    notebook_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)

    def __init__(self, notebook_id, user_id, name):
        self.notebook_id = notebook_id
        self.user_id = user_id
        self.name = name'''

class Notebook_Pages(db.Model):
    __tablename__ = 'Notebook_Pages'
    page_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # notebook_id = db.Column(db.Integer)
    name = db.Column(db.String)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer)


    def __init__(self, name, content, user_id):
        # self.notebook_id = notebook_id
        self.name = name
        self.content = content
        self.user_id = user_id

    def create_page(self):
        db.session.add(self)
        db.session.commit()
        return True

    def all_pages(self):
        pages = Notebook_Pages.query.all()
        page_links = []
        for page in pages:
            page_links.append(page)
        return page_links
    def find_user_pages(self):
        pages = Notebook_Pages.query.filter_by(user_id = self.user_id).all()
        page_links = []
        for page in pages:
            page_links.append(page)
        return page_links

    def find_user_page_by_id(self):
        pages = Notebook_Pages.query.filter_by(user_id=self.user_id).filter_by(page_id=self.page_id).first()
        return pages

    def updatePage(self):
        page_links = self.find_user_pages()
        for page in page_links:
            if str(page.page_id)!=str(self.page_id):
                print(page.page_id==self.page_id)
                continue
            page.content = self.content
            db.session.commit()
            return True
        self.page_id = None
        self.create_page()
        return True

    def get_page_content(self):
        pages = Notebook_Pages.query.filter_by(page_id = self.page_id).first()
        if pages!=None:
            self.name = pages.name
            return pages.content
        else:
            return "No Such Page Exists"

# with app.app_context():
#     db.create_all()
# user = Users("gg", "abc@", "garima", "gupta")
# db.session.add(user)
# db.session.commit()


'''def connectToDatabase():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

 # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_user(user_info):
    """ insert multiple vendors into the vendors table  """
    sql = 'INSERT INTO public."Users"(password, email, "firstName", "lastName") VALUES({}, {}, {}, {})'.format(user_info[0][0], user_info[1][0], user_info[2][0], user_info[3][0])
    print(sql)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        print("going to execute")
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def login_user(input_email, input_password):
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = {} AND password = {}".format(input_email, input_password))
        rows = cur.fetchall()
        if rows == None:
            return False
        else:
            return True

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    connectToDatabase() '''
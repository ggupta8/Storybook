from flask import Flask, request, render_template, session, flash, g
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.static_folder = 'static'
passDict = {'admin':['password', 'adminperson']}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:garima@localhost/storybook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

import databaseCommands

@app.route('/')
def index():
   return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.before_request
def load_user():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/dashboard')
def dashboard():
    if g.user:
        return render_template("dashboard.html")
    return render_template("login.html")
    # return render_template("textEditor.html")

@app.route('/editor', methods=['GET'])
def editor():
    page_id = request.args['page']
    if g.user:
        # links = []
        curr = databaseCommands.Notebook_Pages(None, None, g.user)
        curr.page_id = page_id
        page = curr.find_user_page_by_id()
        if page == None:
            page = "Insert Text Here"
        else:
            page = page.content
        insertedValue = page
        return render_template("textEditor.html", insertedValue = insertedValue, page_id = page_id)
    return render_template("login.html")
    # return render_template("textEditor.html")

@app.route('/pageList', methods=['GET'])
def pageList():
    if g.user:
        curr = databaseCommands.Notebook_Pages(None, None, g.user)
        page_links = curr.find_user_pages()
        newPage = databaseCommands.Notebook_Pages(None, None, g.user)
        newPage.page_id = -2
        nameLink = []
        nameLink.append({"name": "New Page", "link": "/editor?page=-2"})
        for page in page_links:
            nameLink.append({"name": page.name, "link": "/editor?page="+str(page.page_id)})
        return render_template("pageListForUser.html", pages = nameLink)
    return render_template("login.html")


@app.route('/allPages', methods=['GET'])
def allPages():
    curr = databaseCommands.Notebook_Pages(None, None, None)
    page_links = curr.all_pages()

    nameLink = []
    for page in page_links:
        nameLink.append({"name": page.name, "link": "/getPage?page=" + str(page.page_id)})
    return render_template("pageListForUser.html", pages=nameLink)

@app.route('/savePage', methods=['POST'])
def savePage():
    page_id = request.args['page']
    if g.user:
        print(g.user)
        print(request.form["name"])
        page = databaseCommands.Notebook_Pages(request.form["name"], request.form["content"], g.user)
        page.page_id = page_id
        page.updatePage()
        return render_template("textEditor.html")
    return render_template("login.html")

@app.route('/getPage', methods = ['GET'])
def getPage():
    page_id = request.args['page']
    page = databaseCommands.Notebook_Pages(None, None, None)
    page.page_id = page_id
    content = page.get_page_content()
    return render_template("viewPage.html", name = page.name, content=content)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        user = databaseCommands.Users(request.form['password'], request.form['email'], None, None)
        if databaseCommands.Users.login_user(user):
            print(user.user_id)
            session['user'] = user.user_id
            flash('welcome ' + user.firstName)
            return render_template("dashboard.html")
        else:
            flash('wrong password!')
            return render_template("login.html")
    return render_template("login.html")

@app.route('/register')
def register():
    print("hi")
    return render_template("createAccount.html")

@app.route('/createAccount', methods=['POST'])
def createAccount():
    if request.form['password'] != request.form['confirm']:
        flash('password mismatch')
        return render_template("createAccount.html")
    else:
        user = databaseCommands.Users(request.form['password'], request.form['email'], request.form['firstName'],
                                      request.form['lastName'])
        if not databaseCommands.Users.create_user(user):
            flash('user with that email already exists')
            return render_template("createAccount.html")
        else:
            flash('account has been created')
            return render_template("login.html")


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True)
from psycopg2 import connect, extras
import forms
from app import app
from flask import Flask, url_for, render_template, redirect, session, request

conn = connect(database="cat_index", user="postgres", host="/tmp", port="5433")
cur = conn.cursor(cursor_factory=extras.DictCursor)

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index(): 
  form = forms.UrlForm()
  cur.execute("SELECT target FROM url")
  items = cur.fetchall()

  return render_template('index.html', form=form, items=items)

@app.route("/add", methods=["POST"])
def add():
  url = request.form["url"]
  cur.execute("INSERT into url (target) VALUES (%s)", [url])
  conn.commit()
  return redirect(url_for("index"))

from flask import Flask, url_for, render_template, redirect, session, request

@app.route('/', methods=["GET", "POST"])
def index(): 
    return render_template('index.html')

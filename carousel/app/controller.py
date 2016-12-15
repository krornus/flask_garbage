from fake_useragent import UserAgent
from flask import Flask, url_for, render_template, redirect, session, request
from bs4 import BeautifulSoup
import os 
import re
import requests
from app import app
from model import *
import reddit_api

@app.route('/', methods=["GET", "POST"])
def index(): 

    images = []
    other = []

    url = load_params(request)

    api = reddit_api.RedditApi()
    result = api.get_images(url.url)
    if not result:
        result = [""]
        url.sr = url.sr  + " - No results - " + url.url
    

    for image in result:
        if "imgur" in image:
            image = get_imgur_image(image)
        if re.search("gfycat|webm|gifv", image):
            if "imgur" in image:
                image = image.replace(".gifv", ".mp4")
            if "gfycat" in image:
                image = get_gfycat_image(image)
            other.append(image)
        else:
            images.append(image)

    return render_template('index.html', iframes=other, images=images, url=url, cache_bust=os.path.getmtime("app/static/style.css"))

@app.route('/next', methods=["GET", "POST"])
def next(): 
    
    current_url = load_params(request)
    api = reddit_api.RedditApi()
    current_url.after = api.get_next(current_url.url)


    parameters = get_param_string(current_url)

    url = url_for("index") + parameters + "&rand="+ request.args.get("rand") or False 

    return redirect(url)


def load_params(request):
        
    url = reddit_api.RedditUrl(request.args.get('sr') or "cats")

    url.time = request.args.get("t") or "month"
    url.sort = request.args.get("sort") or "top"
    url.query = request.args.get("q") or ""
    url.flair = request.args.get("flair") or ""
    url.self_post = request.args.get("self") or "no"
    url.count = request.args.get("count") or "50"
    url.before = request.args.get("before") 
    url.after = request.args.get("after") or None

    return url

def get_param_string(url):
    
    params = "?sr={}&t={}&sort={}&q={}&flair={}&self={}&count={}"

    params = params.format(url.sr, url.time, url.sort, url.query,
                         url.flair, url.self_post, url.count)

    # these are mutually exclusive   
    if url.after:
        params += "&after=" + url.after

    elif url.before:
        params += "&before=" + url.before

    return params


def get_gfycat_image(url):
    html =  requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    image = soup.find("source")
    
    if image and 'src' in str(image):
        return image['src']
    else:
        return url

def get_imgur_image(url):
    if re.search("imgur.com/.+\..+", url):
        return url

    html =  requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    
    html2 = str(soup.find("div", {"class": "post-image"}))
    soup2 = BeautifulSoup(html2, "lxml")
    image = soup2.find("a")
    if image and 'href' in str(image):
        return image['href']
    else:
        print url 
    return ""

from fake_useragent import UserAgent
from flask import Flask, url_for, render_template, redirect, session, request
from bs4 import BeautifulSoup
import re
import requests
from app import app
from model import *

@app.route('/', methods=["GET", "POST"])
def index(): 
	
    images = []
    other = []
    
    sr = request.args.get('sr') or "cats"
    time = request.args.get("t") or "month"
    after = request.args.get("after") or None
    
    url = 'https://www.reddit.com/r/{}/search?restrict_sr=on&sort=top&t={}' 

    if after:
        url += "&after=" + after

    
    result, sr = get_images(url.format(sr, time))

    for image in result:
	    if re.search("gfycat|webm|gifv", image):
		    other.append(image)
	    else:
		    images.append(image)

    sr = sr.replace("https://www.reddit.com/r/", "").replace("/search?restrict_sr=on&sort=top&t=" + time, "")
	
    return render_template('index.html', iframes=other, images=images, sr=sr, after=after, time=time)

@app.route('/next', methods=["GET", "POST"])
def next(): 
    
    sr = request.args.get('sr') or "cats"
    time = request.args.get('t') or "month"
    after = request.args.get("after") or None
    url = 'https://www.reddit.com/r/{}/search?restrict_sr=on&sort=top&t={}' 

    if after:
        url += "&after=" + after

    after = get_next(url.format(sr,time))
    ai = after.index("after=") + len("after=")
    after = after[ai:]
    
    return redirect(url_for("index", after=after, sr=sr, t=time))

def reddit(url):
    html, sr = open_url(url)

    soup=BeautifulSoup(html, "lxml")
	
    links = soup.find_all("div", {"class":"listing search-result-listing"})
    lsoup = BeautifulSoup(str(links), "lxml")
    results = [ l['href'] for l in lsoup.find_all("a", {"class":"search-link"})]

    images = []
    for img in results:
        if re.search("jpg|png|jpeg|gfycat|gif", img):
            images.append(img)

    return images, sr


def get_images(url):
		if url[0:22] == "https://www.reddit.com":
			return reddit(url)

def get_next(url):
    
    html, sr = open_url(url)
    soup=BeautifulSoup(html, "lxml")
    links = soup.find("a", {"rel":"next"})

    return links['href']

	
def open_url(url):
    ua = UserAgent()

    headers = {'User-Agent': ua.chrome}
    cookies = {}
    response = requests.get(url, headers=headers, cookies=cookies)

    return response.text, response.url


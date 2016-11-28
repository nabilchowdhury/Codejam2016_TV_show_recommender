from app import app, recommend
from flask import Flask, request, render_template
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/post/user', methods=['POST', 'GET'])
def save_user():
    genres = request.form.getlist('genre')
    shows = request.form.getlist('tvshows')
    shows1 = [show for show in shows if show != '']
    rcms = recommend.recommend(genres, shows1)
    # return str(rcms) + str(genres) + str(shows1)
    title, rating, poster, summary = rcms
    # return str([title, rating, poster, summary])
    return render_template('results.html',
            top_title=title,
            top_rating=rating,
            poster=poster,
            top_summary=summary)

import json
import os

_GENRES_ = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime',
          'documentary', 'drama', 'family', 'fantasy', 'game-show', 'history',
          'horror', 'music', 'musical', 'mystery', 'news', 'reality-tv', 'romance',
          'sci-fi','short', 'sport', 'talk-show', 'thriller', 'war', 'western']

with open(os.path.join('app','static', 'tv.json'), 'r') as f:
    tv = json.load(f)

def genre_vec(genres, shows):
    d = dict()
    for g in _GENRES_: d[g] = 0
    for g in   genres: d[g] += 3
    for show in shows:
        if show in tv:
            for g in tv[show]['genres']:
                d[g.lower()] += 1
    return d

def get_tv_scores(input_v, watched_shows):
    def show_vec(k):
        d = dict()
        for g in _GENRES_: d[g] = 0
        for g in tv[k]['genres']:
            d[g.lower()] += 1
        return d

    show_vec_list = list()
    for k in tv:
        if k not in watched_shows:
            rating = float(tv[k]['critic_rating'])
            rating_factor = 1. if rating < 6. else ((rating + 2.) / 8.)
            show_vec_list.append((k, show_vec(k), rating_factor))
    # show_vec_list = [(k, show_vec(k), float(tv[k]['critic_rating'])/6.) for k in tv if k not in watched_shows]
    return ((k,
            sum(int(item[0]*item[1]*v2) for item in zip(input_v.values(), v1.values())))
            for k, v1, v2 in show_vec_list)

def recommend(genres, shows):
    '''
    Get our input (genres, shows). We map these two lists and create a genre vector.

    We now want to rank the tv shows. For every tv show, and for every genre in that show,
    we want to get the value of that genre from the user genre vector and add them up.
    This will represent the tv show's score. Reture score list for tv shows with score greater than 0
    '''

    shws = shows.copy()
    gnrs = genres.copy()
    for k in tv:
        for i, s in enumerate(shws):
            if len(k) > len(s):
                shws[i] = k if s in k else s
            else:
                shws[i] = k if k in s else s

    input_vec = genre_vec(gnrs, shws)

    tv_scores =\
    sorted((scr for scr in get_tv_scores(input_vec, shws) if scr[1] > 0), key=lambda x:x[1])

    # rcms, _ = zip(*tv_scores[-20:]
    # rcms = [(tv[show]['title'], tv[show]['critic_rating'], tv[show]['poster_url'], tv[show]['summary']) for show in rcms]
    # return rcms

    top_show, _ = tv_scores.pop()
    return (tv[top_show]['title'], tv[top_show]['critic_rating'], tv[top_show]['poster_url'], tv[top_show]['summary'])

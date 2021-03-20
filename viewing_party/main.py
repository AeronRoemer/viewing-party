from statistics import mean # new requirement 
from collections import Counter # built in to python
import random 

def create_movie(movie_title, genre, rating):
    if movie_title and genre and rating:
        return {
            "title": movie_title,
            "genre": genre,
            "rating": rating
        }
    return None

def add_to_watched(user_data, movie):
    user_data['watched'].append(movie)
    return user_data

def add_to_watchlist(user_data, movie):
    user_data['watchlist'].append(movie)
    return user_data

def watch_movie(user_data, movie):
    for item in user_data['watchlist']:
        if movie == item['title']:
            user_data['watched'].append(item)
            user_data['watchlist'].remove(item)
    return user_data

def get_watched_avg_rating(user_data):
    if user_data['watched']:
        # using mean() from statistics since numpy mean() takes Array, not List
        return mean(movie['rating'] for movie in user_data['watched']) 
        # list comprehension replaces for loop
    else:
        return 0

def get_most_watched_genre(user_data):
    if not user_data['watched']:
        return None
    else:
        genre_list = [item['genre'] for item in user_data['watched']]
        # returns each genre in a list
        genre_count = Counter(genre_list).most_common() 
        # creates an unordered collection of data with count information from python's
        #  built in Counter from collections module
        return genre_count[0][0]

def get_friend_watched(user_data):
    # gets list of movies friends have watched
    friend_watched = []
    for friend_data in user_data["friends"]:
        for movies in friend_data.values():
            for movie in movies:
                friend_watched.append(movie)
    return friend_watched

def get_unique_watched(user_data):
    # gets movies that user has watched that user's friends haven't
    user_watched = [x for x in user_data['watched']]
    unique_watched = []
    friend_watched = get_friend_watched(user_data)      
    for movie in user_watched:
        if movie not in friend_watched and movie not in unique_watched:
            unique_watched.append(movie)
    return unique_watched

def get_friends_unique_watched(user_data):
    # gets movies that friends have watched but user hasn't
    user_watched = [x for x in user_data['watched']]
    unique_watched = []
    friend_watched = get_friend_watched(user_data) 

    for movie in friend_watched:
        if movie not in user_watched and movie not in unique_watched:
            unique_watched.append(movie)
    return unique_watched

def get_available_recs(user_data):
    recommendations = []
    services = user_data['subscriptions']
    for friend_data in user_data["friends"]:
        for movies in friend_data.values():
            for movie in movies:
                if movie['host'] in services and movie not in recommendations:
                    recommendations.append(movie)
    
    return recommendations

def get_new_rec_by_genre(user_data):
    most_watched = get_most_watched_genre(user_data)
    possible_recs = get_friends_unique_watched(user_data)
    recs = []
    for movie in possible_recs:
        if most_watched in movie.values():
            recs.append(movie)
    return recs

def get_rec_from_favorites(user_data):
    possible_rec = user_data['favorites']
    friend_watched = get_friend_watched(user_data)
    recs = []
    for item in possible_rec:
        if item not in friend_watched:
            recs.append(item)
    return recs
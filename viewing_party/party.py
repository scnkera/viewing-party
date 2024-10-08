# ------------- WAVE 1 --------------------

def create_movie(title, genre, rating):
    movie_dict = {}

    if not title or not genre or not rating:
        return None
    else:
        movie_dict['title'] = title
        movie_dict['genre'] = genre
        movie_dict['rating'] = rating
    
    return movie_dict

def add_to_watched(user_data, movie):

    user_data["watched"].append(movie)
    
    return user_data

def add_to_watchlist(user_data, movie):

    user_data["watchlist"].append(movie)
    
    return user_data

def watch_movie(user_data, title):

    for movie in user_data["watchlist"]:
        if movie["title"] == title:
            user_data["watchlist"].remove(movie)
            user_data["watched"].append(movie)
            break
    return user_data

# -----------------------------------------
# ------------- WAVE 2 --------------------
# -----------------------------------------

def get_watched_avg_rating(user_data):

    if not user_data["watched"]:
        return 0.0
    
    total_rating = 0
    for movie in user_data["watched"]:
        total_rating += movie["rating"] 
            
    average = total_rating / len(user_data["watched"])

    return average

def get_most_watched_genre(user_data):
    genre_count = {"Fantasy": 0, "Intrigue": 0, "Action": 0} #change method so that other genres can be included

    if not user_data["watched"]:
        return None 
    
    for movie in user_data["watched"]:
        genre = movie["genre"]
        if genre in genre_count:
            genre_count[genre] += 1   
    top_genre = max(genre_count, key=genre_count.get)

    return top_genre

# -----------------------------------------
# ------------- WAVE 3 --------------------
# -----------------------------------------
def get_unique_watched(user_data):

    movies_not_watched_by_friends = []

    for movie_watched_by_user in user_data["watched"]:
        watched_by_any_friend = False

        # checks if the movie is has been watched by a friend
        for friend in user_data["friends"]:
            if movie_watched_by_user in friend["watched"]:
                watched_by_any_friend = True
                break

        # If no friend has watched it, adds it to the final list
        if not watched_by_any_friend:
            movies_not_watched_by_friends.append(movie_watched_by_user)
    
    return movies_not_watched_by_friends

def get_friends_unique_watched(user_data):

    movies_watched_by_friends_not_user = []

    # loops through each friend's watched list
    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            # appends to list if 1) movie is not in the user's watched list and 2) not already in the result list
            if movie not in user_data["watched"] and movie not in movies_watched_by_friends_not_user:
                movies_watched_by_friends_not_user.append(movie)
    
    return movies_watched_by_friends_not_user
        
# -----------------------------------------
# ------------- WAVE 4 --------------------
# -----------------------------------------

def get_available_recs(user_data):
    subscriptions = set(user_data.get("subscriptions", []))

    recommended_movies = set()  # Using a set to ensure uniqueness
    user_watched = set()  # Track movies the user has already watched

    # Populate user_watched set with movie titles from user_data
    for movie in user_data.get("watched"):
        if "title" in movie:
            user_watched.add(movie["title"])
  
    # Loop through each friend and their watched movies
    for friend in user_data.get("friends"):
        for movie in friend.get("watched"):
                # Only add the movie if it's hosted on a subscribed platform and not watched by the user
            if movie["host"] in subscriptions and movie["title"] not in user_watched:
                recommended_movies.add((movie["title"], movie["host"], movie["rating"], movie["genre"]))

    # Convert the set of tuples back to a list of dictionaries, including the 'genre' key
    updated_recommendation = [
        {"title": title, "host": host, "rating": rating, "genre": genre}
        for title, host, rating, genre in recommended_movies
    ]

    return updated_recommendation
 
# -----------------------------------------
# ------------- WAVE 5 --------------------
# -----------------------------------------
def get_new_rec_by_genre(user_data):
    watched_movies = user_data["watched"]
    if not watched_movies:
        return []  # If there are no watched movies, return an empty list

    # Count the genres of watched movies
    genre_counter = {}
    for movie in watched_movies:
        genre = movie["genre"]
        if genre not in genre_counter:
            genre_counter[genre] = 0
        genre_counter[genre] += 1

    # Get the most common genre
    top_genre = max(genre_counter, key=genre_counter.get)

    recommendations = []  # List to store recommendations
    watched_titles = []  # List to store titles the user has watched

    for movie in watched_movies:
        watched_titles.append(movie["title"])

    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            if (movie["genre"] == top_genre and 
                movie["title"] not in watched_titles):
                # Check for duplicates 
                if movie not in recommendations:
                    recommendations.append(movie)

    return recommendations

def get_rec_from_favorites(user_data):

    favorites = user_data["favorites"]
    if not favorites:
        return []

    friends_watched_titles = []  
    recommendations = []

    for friend in user_data["friends"]:
        for movie in friend["watched"]:
            friends_watched_titles.append(movie["title"])

    for movie in favorites:
        if movie["title"] not in friends_watched_titles:
            recommendations.append(movie)

    return recommendations
from flask import Flask, request, jsonify
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the TMDB API endpoint and headers
tmdb_endpoint = 'https://api.themoviedb.org/3/discover/movie'
tmdb_headers = {
    'Content-Type': 'application/json;charset=utf-8'
}

# Define the TMDB API query parameters
tmdb_params = {
    'api_key': '33bab856db9d13e9ecc98e49179feae6',  
    'sort_by': 'popularity.desc',
    'include_adult': 'false',
    'include_video': 'false',
    'page': '1',
    'vote_count.gte': '50',
    'with_genres': None
}

def get_genre_ids(genre_names):
    # Define the API endpoint and headers
    endpoint = 'https://api.themoviedb.org/3/genre/movie/list'
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }

    # Define the API query parameters
    params = {
        'api_key': '33bab856db9d13e9ecc98e49179feae6',  
    }

    # Make the API request and get the response
    response = requests.get(endpoint, headers=headers, params=params)

    # Parse the response and find the matching genre IDs
    if response.status_code == 200:
        data = json.loads(response.text)
        genres = data['genres']
        genre_ids = []
        genredict = {}
        for genre_name in genre_names:
            for genre in genres:
                if genre['name'].lower() == genre_name.lower():
                    genre_ids.append(genre['id'])
                    genredict[genre['id']] = genre_name
                    break
        return genre_ids, genredict
    else:
        return []

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Parse the JSON payload from the request
    data = request.get_json()

    # Get the list of liked genre names and movie names from the payload
    genre_names = data.get('liked_genres', [])
    movie_names = data.get('liked_movies', [])

    # Convert the genre names to genre IDs using the get_genre_ids function
    genre_ids, genredict = get_genre_ids(genre_names)

    # Define a dictionary to hold the recommended movies for each genre
    recommendations = {}

    # Get the top 10 recommended movies for each genre
    for genre_id in genre_ids:
        # Set the genre ID in the TMDB API query parameters
        tmdb_params['with_genres'] = str(genre_id)

        # Make the API request and get the response
        response = requests.get(tmdb_endpoint, headers=tmdb_headers, params=tmdb_params)

        # Parse the response and extract the top 10 recommended movies
        if response.status_code == 200:
            data = json.loads(response.text)
            results = data['results']
            movie_titles = [movie['title'] for movie in results[:5]]
            recommendations[genredict[genre_id]] = movie_titles

    # Return the recommendations as a JSON response
    return jsonify(recommendations)
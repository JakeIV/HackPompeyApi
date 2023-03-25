import requests
import json

# Define the URL of the Flask server
url = 'http://localhost:5000/recommendations'

# Define the example list of liked genres and movies
liked_genres = ['Action', 'Adventure', 'Comedy', 'Drama']
liked_movies = ['The Dark Knight', 'The Lord of the Rings: The Return of the King', 'The Hangover', 'The Shawshank Redemption']

# Define the JSON payload to send to the server
payload = {
    'liked_genres': liked_genres,
    'liked_movies': liked_movies
}

# Send the POST request to the Flask server and get the response
response = requests.post(url, json=payload)

# Parse the response and print the recommended movies for each genre
if response.status_code == 200:
    data = json.loads(response.text)
    for genre, movies in data.items():
        print(f"{genre}: {', '.join(movies)}")
else:
    print('Error:', response.status_code)
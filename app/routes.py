
from flask import jsonify, render_template, request
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import pickle
import os

import requests
from app import app

movies_data = pd.read_csv('movies.csv')  # Replace 'movies.csv' with your movie data file
with open('movie_recommendation_model.pkl', 'rb') as model_file:
    cosine_similarity_model = pickle.load(model_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['movie_name']

    corrected_title = process.extractOne(user_input, movies_data['title'], scorer=fuzz.token_sort_ratio)

    if corrected_title[1] < 60:
        return render_template('recommendations.html', user_input=user_input, recommendations=["No matches found"])

    corrected_title = corrected_title[0]

    # Find the index of the corrected movie title
    index_of_the_movie = movies_data[movies_data['title'] == corrected_title].index[0]

    # Try to find an exact match first
    exact_match = movies_data[movies_data['title'] == user_input]

    if not exact_match.empty:
        index_of_the_movie = exact_match.index[0]
    else:
        # If no exact match, perform a case-insensitive and fuzzy search
        close_matches = process.extractBests(user_input, movies_data['title'], score_cutoff=60)
        if not close_matches:
            return render_template('recommendations.html', user_input=user_input, recommendations=["No matches found"])

        index_of_the_movie = close_matches[0][2]

    # Get the similarity scores for the selected movie
    similarity_scores = list(enumerate(cosine_similarity_model[index_of_the_movie]))

    # Sort movies based on similarity
    sorted_similar_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 similar movies
    top_similar_movies = sorted_similar_movies[1:11]  # Exclude the selected movie itself

    # Get the titles of the top similar movies
    recommended_movies = [movies_data.iloc[movie[0]]['title'] for movie in top_similar_movies]

    return render_template('recommendations.html', user_input=user_input,corrected_title=corrected_title, recommendations=recommended_movies)

@app.route('/movie_details/<title>', methods=['GET'])
def movie_details(title):
    # Search for movie details based on the title
    movie = movies_data[movies_data['title'] == title].to_dict(orient='records')
    if movie:
        return render_template('movie_details.html', movie=movie[0])
    else:
        return "Movie details not found",404
    

    movie_details = {
        'title': title,
        'overview': 'Movie overview here',
        'genre': 'Action',
        'cast': 'Actor 1, Actor 2',
        'director': 'Director Name',
        'popularity': 'High',
        'release_date': '2023-01-01',
    }

    return render_template('movie_details.html', movie_details=movie_details)
'''
@app.route('/suggest_movies', methods=['POST'])
def suggest_movies():
    print(request.headers)
    user_input = request.get_json()
    print(user_input) 
    # Filter movie titles that start with or contain the user input (case-insensitive)
    suggestions = [title for title in movies_data['title'] if user_input.lower() in title.lower()]

    # Limit the number of suggestions (e.g., top 10)
    suggestions = suggestions[:5]

    # Return suggestions as JSON


    return jsonify({'suggestions': suggestions})

'''


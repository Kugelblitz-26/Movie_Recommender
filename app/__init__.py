import pickle
import os
import pandas as pd

from flask import Flask

app = Flask(__name__)

from app import routs  # Import routes after creating the app instance to avoid circular imports

# Load the movie recommendation model
movies_data = pd.read_csv('movies.csv')  # Replace 'movies.csv' with your movie data file
with open('movie_recommendation_model.pkl', 'rb') as model_file:
    cosine_similarity_model = pickle.load(model_file)
